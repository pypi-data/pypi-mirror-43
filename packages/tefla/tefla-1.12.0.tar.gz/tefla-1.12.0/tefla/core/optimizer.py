from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import types
import six
import contextlib
import numbers
import tensorflow as tf
import collections
from tensorflow.python.training import optimizer
from tensorflow.python.training import saver
from tensorflow.python.training import training_ops
from ..utils.util import GetTensorOpName, ListUnion, Interface, BatchClipByL2norm, AddGaussianNoise
from . import logger as log

__all__ = ["VariableClippingOptimizer"]
ClipOption = collections.namedtuple("ClipOption", ["l2norm_bound", "clip"])
OrderedDict = collections.OrderedDict

GLOBAL_VARIABLE_NAME = 'global_center_variable'


class RMSPropunroll(optimizer.Optimizer):

  def __init__(self, learning_rate=1e-4, use_locking=False, name='SMORMS3'):
    super(RMSPropunroll, self).__init__(use_locking, name)
    self._learning_rate = learning_rate
    self._eps_t = None
    self._g2 = None
    self._g = None
    self._xi = None

  def _prepare(self):
    if isinstance(self._learning_rate, numbers.Number):
      self._eps_placeholder = None
      self._eps_op = None
      self._eps_t = tf.convert_to_tensor(self._learning_rate, name="epsilon")
    else:
      self._eps_placeholder = tf.placeholder(self._learning_rate.dtype, [1], name='eps_placeholder')
      self._eps_op = tf.assign(self._learning_rate, self._eps_placeholder)
      self._eps_t = self._learning_rate

  def _create_slots(self, var_list):
    if self._g2 is None:
      with tf.Graph().colocate_with(var_list[0]):
        for v in var_list:
          self._xi = self._zeros_slot(v, "xi", self._name)
          self._g = self._zeros_slot(v, "g", self._name)
          self._g2 = self._zeros_slot(v, "g2", self._name)

  def _optimizer_step(self, grad, var, xi, g, g2):
    eps = 1e-16
    r_t = 1. / (xi + 1.)
    g_t = (1. - r_t) * g + r_t * grad
    g2_t = (1. - r_t) * g2 + r_t * grad**2
    var_t = var - grad * tf.minimum(g_t * g_t / (g2_t + eps), self._eps_t) / \
        (tf.sqrt(g2_t + eps) + eps)
    xi_t = 1 + xi * (1 - g_t * g_t / (g2_t + eps))
    return var_t, xi_t, g_t, g2_t

  def _apply_dense(self, grad, var):
    xi = self.get_slot(var, "xi")
    g = self.get_slot(var, "g")
    g2 = self.get_slot(var, "g2")
    var_t, xi_t, g_t, g2_t = self._optimizer_step(grad, var, xi, g, g2)

    # update helper variables
    xi_update = tf.assign(xi, xi_t, use_locking=self._use_locking)
    g_update = tf.assign(g, g_t, use_locking=self._use_locking)
    g2_update = tf.assign(g2, g2_t, use_locking=self._use_locking)
    var_update = tf.assign(var, var_t, use_locking=self._use_locking)

    all_updates = [xi_update, g_update, g2_update, var_update]
    return tf.group(*all_updates)

  def _apply_sparse(self, grad, var):
    raise NotImplementedError("apply_sparse not yet implemented")

  @property
  def eps_op(self):
    return self._eps_op, self._eps_placeholder

  def unroll(self, grads, var_list, opt_vars=None):
    next_opt_vars = []
    next_vars = []
    for i, (grad, var) in enumerate(zip(grads, var_list)):
      if opt_vars is None:
        xi = self.get_slot(var, "xi")
        g = self.get_slot(var, "g")
        g2 = self.get_slot(var, "g2")
      else:
        xi, g, g2 = opt_vars[i]
      var_t, xi_t, g_t, g2_t = self._optimizer_step(grad, var, xi, g, g2)
      next_opt_vars.append([xi_t, g_t, g2_t])
      next_vars.append(var_t)
    return next_vars, next_opt_vars


class AdagradDAOptimizer(optimizer.Optimizer):
  """Adagrad Dual Averaging algorithm for sparse linear models.

  See this [paper](http://www.jmlr.org/papers/volume12/duchi11a/duchi11a.pdf).
  This optimizer takes care of regularization of unseen features in a mini batch
  by updating them when they are seen with a closed form update rule that is
  equivalent to having updated them on every mini-batch.
  AdagradDA is typically used when there is a need for large sparsity in the
  trained model. This optimizer only guarantees sparsity for linear models. Be
  careful when using AdagradDA for deep networks as it will require careful
  initialization of the gradient accumulators for it to train.
  """

  def __init__(self,
               learning_rate,
               global_step,
               initial_gradient_squared_accumulator_value=0.1,
               l1_regularization_strength=0.0,
               l2_regularization_strength=0.0,
               use_locking=False,
               name="AdagradDA"):
    """Construct a new AdagradDA optimizer.

    Args:
      learning_rate: A `Tensor` or a floating point value.  The learning rate.
      global_step: A `Tensor` containing the current training step number.
      initial_gradient_squared_accumulator_value: A floating point value.
        Starting value for the accumulators, must be positive.
      l1_regularization_strength: A float value, must be greater than or
        equal to zero.
      l2_regularization_strength: A float value, must be greater than or
        equal to zero.
      use_locking: If `True` use locks for update operations.
      name: Optional name prefix for the operations created when applying
        gradients.  Defaults to "AdagradDA".
    Raises:
      ValueError: If the `initial_gradient_squared_accumulator_value` is
      invalid.
    """
    if initial_gradient_squared_accumulator_value <= 0.0:
      raise ValueError("initial_gradient_squared_accumulator_value must be"
                       "positive: %s" % initial_gradient_squared_accumulator_value)
    super(AdagradDAOptimizer, self).__init__(use_locking, name)
    self._learning_rate = learning_rate
    self._initial_gradient_squared_accumulator_value = (initial_gradient_squared_accumulator_value)
    # Created in Initialize.
    self._learning_rate_tensor = None
    self._l1_regularization_strength = l1_regularization_strength
    self._l2_regularization_strength = l2_regularization_strength
    self._global_step = global_step

  def _create_slots(self, var_list):
    for v in var_list:
      with tf.Graph().colocate_with(v):
        g_val = tf.constant(0.0, shape=v.get_shape(), dtype=v.dtype.base_dtype)
        gg_val = tf.constant(
            self._initial_gradient_squared_accumulator_value,
            shape=v.get_shape(),
            dtype=v.dtype.base_dtype)
      self._get_or_make_slot(v, g_val, "gradient_accumulator", self._name)
      self._get_or_make_slot(v, gg_val, "gradient_squared_accumulator", self._name)

  def _prepare(self):
    self._learning_rate_tensor = tf.convert_to_tensor(self._learning_rate, name="learning_rate")

  def _apply_dense(self, grad, var):
    g_acc = self.get_slot(var, "gradient_accumulator")
    gg_acc = self.get_slot(var, "gradient_squared_accumulator")
    with tf.device(grad[0].device):
      global_step = tf.identity(self._global_step) + 1
    return training_ops.apply_adagrad_da(
        var,
        g_acc,
        gg_acc,
        grad,
        tf.cast(self._learning_rate_tensor, var.dtype.base_dtype),
        tf.cast(self._l1_regularization_strength, var.dtype.base_dtype),
        tf.cast(self._l2_regularization_strength, var.dtype.base_dtype),
        global_step,
        use_locking=self._use_locking)

  def _resource_apply_dense(self, grad, var):
    g_acc = self.get_slot(var, "gradient_accumulator")
    gg_acc = self.get_slot(var, "gradient_squared_accumulator")
    with tf.device(grad[0].device):
      global_step = tf.identity(self._global_step) + 1
    return training_ops.resource_apply_adagrad_da(
        var.handle,
        g_acc.handle,
        gg_acc.handle,
        grad,
        tf.cast(self._learning_rate_tensor, grad.dtype.base_dtype),
        tf.cast(self._l1_regularization_strength, grad.dtype.base_dtype),
        tf.cast(self._l2_regularization_strength, grad.dtype.base_dtype),
        global_step,
        use_locking=self._use_locking)

  def _apply_sparse(self, grad, var):
    g_acc = self.get_slot(var, "gradient_accumulator")
    gg_acc = self.get_slot(var, "gradient_squared_accumulator")
    with tf.device(grad[0].device):
      global_step = tf.identity(self._global_step) + 1
    return training_ops.sparse_apply_adagrad_da(
        var,
        g_acc,
        gg_acc,
        grad.values,
        grad.indices,
        tf.cast(self._learning_rate_tensor, var.dtype.base_dtype),
        tf.cast(self._l1_regularization_strength, var.dtype.base_dtype),
        tf.cast(self._l2_regularization_strength, var.dtype.base_dtype),
        global_step,
        use_locking=self._use_locking)

  def _resource_apply_sparse(self, grad, var, indices):
    g_acc = self.get_slot(var, "gradient_accumulator")
    gg_acc = self.get_slot(var, "gradient_squared_accumulator")
    with tf.device(grad[0].device):
      global_step = tf.identity(self._global_step) + 1
    return training_ops.resource_sparse_apply_adagrad_da(
        var.handle,
        g_acc.handle,
        gg_acc.handle,
        grad,
        indices,
        tf.cast(self._learning_rate_tensor, grad.dtype),
        tf.cast(self._l1_regularization_strength, grad.dtype),
        tf.cast(self._l2_regularization_strength, grad.dtype),
        global_step,
        use_locking=self._use_locking)


class DPGradientDescentOptimizer(tf.train.GradientDescentOptimizer):
  """Differentially private gradient descent optimizer."""

  def __init__(self,
               learning_rate,
               eps_delta,
               sanitizer,
               sigma=None,
               use_locking=False,
               name="DPGradientDescent",
               batches_per_lot=1):
    """Construct a differentially private gradient descent optimizer. The
    optimizer uses fixed privacy budget for each batch of training.

    Args:
      learning_rate: for GradientDescentOptimizer.
      eps_delta: EpsDelta pair for each epoch.
      sanitizer: for sanitizing the graident.
      sigma: noise sigma. If None, use eps_delta pair to compute sigma;
        otherwise use supplied sigma directly.
      use_locking: use locking.
      name: name for the object.
      batches_per_lot: Number of batches in a lot.
    """

    super(DPGradientDescentOptimizer, self).__init__(learning_rate, use_locking, name)

    # Also, if needed, define the gradient accumulators
    self._batches_per_lot = batches_per_lot
    self._grad_accum_dict = {}
    if batches_per_lot > 1:
      self._batch_count = tf.Variable(1, dtype=tf.int32, trainable=False, name="batch_count")
      var_list = tf.trainable_variables()
      with tf.variable_scope("grad_acc_for"):
        for var in var_list:
          v_grad_accum = tf.Variable(tf.zeros_like(var), trainable=False, name=GetTensorOpName(var))
          self._grad_accum_dict[var.name] = v_grad_accum

    self._eps_delta = eps_delta
    self._sanitizer = sanitizer
    self._sigma = sigma

  def compute_sanitized_gradients(self, loss, var_list=None, add_noise=True):
    """Compute the sanitized gradients.

    Args:
      loss: the loss tensor.
      var_list: the optional variables.
      add_noise: if true, then add noise. Always clip.

    Returns:
      a pair of (list of sanitized gradients) and privacy spending accumulation
      operations.

    Raises:
      TypeError: if var_list contains non-variable.
    """

    self._assert_valid_dtypes([loss])

    xs = [tf.convert_to_tensor(x) for x in var_list]
    px_grads = PerExampleGradients(loss, xs)
    sanitized_grads = []
    for px_grad, v in zip(px_grads, var_list):
      tensor_name = GetTensorOpName(v)
      sanitized_grad = self._sanitizer.sanitize(
          px_grad,
          self._eps_delta,
          sigma=self._sigma,
          tensor_name=tensor_name,
          add_noise=add_noise,
          num_examples=self._batches_per_lot * tf.slice(tf.shape(px_grad), [0], [1]))
      sanitized_grads.append(sanitized_grad)

    return sanitized_grads

  def minimize(self, loss, global_step=None, var_list=None, name=None):
    """Minimize using sanitized gradients. This gets a var_list which is the
    list of trainable variables. For each var in var_list, we defined a
    grad_accumulator variable during init. When batches_per_lot > 1, we
    accumulate the gradient update in those. At the end of each lot, we apply
    the update back to the variable. This has the effect that for each lot we
    compute gradients at the point at the beginning of the lot, and then apply
    one update at the end of the lot. In other words, semantically, we are
    doing SGD with one lot being the equivalent of one usual batch of size.

    batch_size * batches_per_lot.
    This allows us to simulate larger batches than our memory size would permit.
    The lr and the num_steps are in the lot world.

    Args:
      loss: the loss tensor.
      global_step: the optional global step.
      var_list: the optional variables.
      name: the optional name.

    Returns:
      the operation that runs one step of DP gradient descent.
    """

    # First validate the var_list

    if var_list is None:
      var_list = tf.trainable_variables()
    for var in var_list:
      if not isinstance(var, tf.Variable):
        raise TypeError("Argument is not a variable.Variable: %s" % var)

    # Modification: apply gradient once every batches_per_lot many steps.
    # This may lead to smaller error

    if self._batches_per_lot == 1:
      sanitized_grads = self.compute_sanitized_gradients(loss, var_list=var_list)

      grads_and_vars = zip(sanitized_grads, var_list)
      self._assert_valid_dtypes([v for g, v in grads_and_vars if g is not None])

      apply_grads = self.apply_gradients(grads_and_vars, global_step=global_step, name=name)
      return apply_grads

    # Condition for deciding whether to accumulate the gradient
    # or actually apply it.
    # we use a private self_batch_count to keep track of number of batches.
    # global step will count number of lots processed.

    update_cond = tf.equal(
        tf.constant(0), tf.mod(self._batch_count, tf.constant(self._batches_per_lot)))

    # Things to do for batches other than last of the lot.
    # Add non-noisy clipped grads to shadow variables.

    def non_last_in_lot_op(loss, var_list):
      """Ops to do for a typical batch. For a batch that is not the last one in
      the lot, we simply compute the sanitized gradients and apply them to the
      grad_acc variables.

      Args:
        loss: loss function tensor
        var_list: list of variables

      Returns:
        A tensorflow op to do the updates to the gradient accumulators
      """
      sanitized_grads = self.compute_sanitized_gradients(loss, var_list=var_list, add_noise=False)

      update_ops_list = []
      for var, grad in zip(var_list, sanitized_grads):
        grad_acc_v = self._grad_accum_dict[var.name]
        update_ops_list.append(grad_acc_v.assign_add(grad))
      update_ops_list.append(self._batch_count.assign_add(1))
      return tf.group(*update_ops_list)

    # Things to do for last batch of a lot.
    # Add noisy clipped grads to accumulator.
    # Apply accumulated grads to vars.

    def last_in_lot_op(loss, var_list, global_step):
      """Ops to do for last batch in a lot. For the last batch in the lot, we
      first add the sanitized gradients to the gradient acc variables, and then
      apply these values over to the original variables (via an apply gradient)

      Args:
        loss: loss function tensor
        var_list: list of variables
        global_step: optional global step to be passed to apply_gradients

      Returns:
        A tensorflow op to push updates from shadow vars to real vars.
      """

      # We add noise in the last lot. This is why we need this code snippet
      # that looks almost identical to the non_last_op case here.
      sanitized_grads = self.compute_sanitized_gradients(loss, var_list=var_list, add_noise=True)

      normalized_grads = []
      for var, grad in zip(var_list, sanitized_grads):
        grad_acc_v = self._grad_accum_dict[var.name]
        # To handle the lr difference per lot vs per batch, we divide the
        # update by number of batches per lot.
        normalized_grad = tf.div(grad_acc_v.assign_add(grad), tf.to_float(self._batches_per_lot))

        normalized_grads.append(normalized_grad)

      with tf.control_dependencies(normalized_grads):
        grads_and_vars = zip(normalized_grads, var_list)
        self._assert_valid_dtypes([v for g, v in grads_and_vars if g is not None])
        apply_san_grads = self.apply_gradients(
            grads_and_vars, global_step=global_step, name="apply_grads")

      # Now reset the accumulators to zero
      resets_list = []
      with tf.control_dependencies([apply_san_grads]):
        for _, acc in self._grad_accum_dict.items():
          reset = tf.assign(acc, tf.zeros_like(acc))
          resets_list.append(reset)
      resets_list.append(self._batch_count.assign_add(1))

      last_step_update = tf.group(*([apply_san_grads] + resets_list))
      return last_step_update

    update_op = tf.cond(update_cond, lambda: last_in_lot_op(loss, var_list, global_step),
                        lambda: non_last_in_lot_op(loss, var_list))

    return tf.group(update_op)


class PXGRegistry(object):
  """Per-Example Gradient registry.

  Maps names of ops to per-example gradient rules for those ops. These
  rules are only needed for ops that directly touch values that are
  shared between examples. For most machine learning applications, this
  means only ops that directly operate on the parameters. See
  http://arxiv.org/abs/1510.01799 for more information, and please
  consider citing that tech report if you use this function in published
  research.
  """

  def __init__(self):
    self.d = OrderedDict()

  def __call__(self, op, colocate_gradients_with_ops=False, gate_gradients=False):
    if op.node_def.op not in self.d:
      raise NotImplementedError("No per-example gradient rule registered "
                                "for " + op.node_def.op + " in pxg_registry.")
    return self.d[op.node_def.op](op, colocate_gradients_with_ops, gate_gradients)

  def Register(self, op_name, pxg_class):
    """Associates `op_name` key with `pxg_class` value.

    Registers `pxg_class` as the class that will be called to perform
    per-example differentiation through ops with `op_name`.
    Args:
      op_name: String op name.
      pxg_class: An instance of any class with the same signature as MatMulPXG.
    """
    self.d[op_name] = pxg_class


pxg_registry = PXGRegistry()


class MatMulPXG(object):
  """Per-example gradient rule for MatMul op."""

  def __init__(self, op, colocate_gradients_with_ops=False, gate_gradients=False):
    """Construct an instance of the rule for `op`.

    Args:
        op: The Operation to differentiate through.
        colocate_gradients_with_ops: currently unsupported
        gate_gradients: currently unsupported
    """
    assert op.node_def.op == "MatMul"
    self.op = op
    self.colocate_gradients_with_ops = colocate_gradients_with_ops
    self.gate_gradients = gate_gradients

  def __call__(self, x, z_grads):
    """Build the graph for the per-example gradient through the op. Assumes
    that the MatMul was called with a design matrix with examples in rows as
    the first argument and parameters as the second argument.

    Args:
        x: The Tensor to differentiate with respect to. This tensor must
         represent the weights.
        z_grads: The list of gradients on the output of the op.

    Returns:
        x_grads: A Tensor containing the gradient with respect to `x` for
          each example. This is a 3-D tensor, with the first axis corresponding
         to examples and the remaining axes matching the shape of x.
    """
    idx = list(self.op.inputs).index(x)
    assert idx != -1
    assert len(z_grads) == len(self.op.outputs)
    assert idx == 1  # We expect weights to be arg 1
    # We don't expect anyone to per-example differentiate with repsect
    # to anything other than the weights.
    x, _ = self.op.inputs
    z_grads, = z_grads
    x_expanded = tf.expand_dims(x, 2)
    z_grads_expanded = tf.expand_dims(z_grads, 1)
    return tf.multiply(x_expanded, z_grads_expanded)


pxg_registry.Register("MatMul", MatMulPXG)


class Conv2DPXG(object):
  """Per-example gradient rule of Conv2d op.

  Same interface as MatMulPXG.
  """

  def __init__(self, op, colocate_gradients_with_ops=False, gate_gradients=False):

    assert op.node_def.op == "Conv2D"
    self.op = op
    self.colocate_gradients_with_ops = colocate_gradients_with_ops
    self.gate_gradients = gate_gradients

  def _PxConv2DBuilder(self, input_, w, strides, padding):
    """conv2d run separately per example, to help compute per-example
    gradients.

    Args:
        input_: tensor containing a minibatch of images / feature maps.
              Shape [batch_size, rows, columns, channels]
        w: convolution kernels. Shape
          [kernel rows, kernel columns, input channels, output channels]
        strides: passed through to regular conv_2d
        padding: passed through to regular conv_2d

    Returns:
        conv: the output of the convolution.
           single tensor, same as what regular conv_2d does
        w_px: a list of batch_size copies of w. each copy was used
           for the corresponding example in the minibatch.
           calling tf.gradients on the copy gives the gradient for just
                  that example.
    """
    input_shape = [int(e) for e in input_.get_shape()]
    batch_size = input_shape[0]
    input_px = [
        tf.slice(input_, [example] + [0] * 3, [1] + input_shape[1:]) for example in range(batch_size)
    ]
    for input_x in input_px:
      assert int(input_x.get_shape()[0]) == 1
    w_px = [tf.identity(w) for example in range(batch_size)]
    conv_px = [
        tf.nn.conv2d(input_x, w_x, strides=strides, padding=padding)
        for input_x, w_x in zip(input_px, w_px)
    ]
    for conv_x in conv_px:
      num_x = int(conv_x.get_shape()[0])
      assert num_x == 1, num_x
    assert len(conv_px) == batch_size
    conv = tf.concat(axis=0, values=conv_px)
    assert int(conv.get_shape()[0]) == batch_size
    return conv, w_px

  def __call__(self, w, z_grads):
    idx = list(self.op.inputs).index(w)
    # Make sure that `op` was actually applied to `w`
    assert idx != -1
    assert len(z_grads) == len(self.op.outputs)
    # The following assert may be removed when we are ready to use this
    # for general purpose code.
    # This assert is only expected to hold in the contex of our preliminary
    # MNIST experiments.
    assert idx == 1  # We expect convolution weights to be arg 1

    images, filters = self.op.inputs
    strides = self.op.get_attr("strides")
    padding = self.op.get_attr("padding")
    # Currently assuming that one specifies at most these four arguments and
    # that all other arguments to conv2d are set to default.

    conv, w_px = self._PxConv2DBuilder(images, filters, strides, padding)
    z_grads, = z_grads

    gradients_list = tf.gradients(
        conv,
        w_px,
        z_grads,
        colocate_gradients_with_ops=self.colocate_gradients_with_ops,
        gate_gradients=self.gate_gradients)

    return tf.stack(gradients_list)


pxg_registry.Register("Conv2D", Conv2DPXG)


class AddPXG(object):
  """Per-example gradient rule for Add op.

  Same interface as MatMulPXG.
  """

  def __init__(self, op, colocate_gradients_with_ops=False, gate_gradients=False):

    assert op.node_def.op == "Add"
    self.op = op
    self.colocate_gradients_with_ops = colocate_gradients_with_ops
    self.gate_gradients = gate_gradients

  def __call__(self, x, z_grads):
    idx = list(self.op.inputs).index(x)
    # Make sure that `op` was actually applied to `x`
    assert idx != -1
    assert len(z_grads) == len(self.op.outputs)
    # The following assert may be removed when we are ready to use this
    # for general purpose code.
    # This assert is only expected to hold in the contex of our preliminary
    # MNIST experiments.
    assert idx == 1  # We expect biases to be arg 1
    # We don't expect anyone to per-example differentiate with respect
    # to anything other than the biases.
    x, _ = self.op.inputs
    z_grads, = z_grads
    return z_grads


pxg_registry.Register("Add", AddPXG)


def PerExampleGradients(ys,
                        xs,
                        grad_ys=None,
                        name="gradients",
                        colocate_gradients_with_ops=False,
                        gate_gradients=False):
  """Symbolic differentiation, separately for each example.

  Matches the interface of tf.gradients, but the return values each have
  an additional axis corresponding to the examples. Assumes that the
  cost in `ys` is additive across examples. e.g., no batch
  normalization. Individual rules for each op specify their own
  assumptions about how examples are put into tensors.
  """

  # Find the interface between the xs and the cost
  for x in xs:
    assert isinstance(x, tf.Tensor), type(x)
  interface = Interface(ys, xs)
  merged_interface = []
  for x in xs:
    merged_interface = ListUnion(merged_interface, interface[x])
  # Differentiate with respect to the interface
  interface_gradients = tf.gradients(
      ys,
      merged_interface,
      grad_ys=grad_ys,
      name=name,
      colocate_gradients_with_ops=colocate_gradients_with_ops,
      gate_gradients=gate_gradients)
  grad_dict = OrderedDict(zip(merged_interface, interface_gradients))
  # Build the per-example gradients with respect to the xs
  if colocate_gradients_with_ops:
    raise NotImplementedError("The per-example gradients are not yet " "colocated with ops.")
  if gate_gradients:
    raise NotImplementedError("The per-example gradients are not yet " "gated.")
  out = []
  for x in xs:
    zs = interface[x]
    ops = []
    for z in zs:
      ops = ListUnion(ops, [z.op])
    if len(ops) != 1:
      raise NotImplementedError("Currently we only support the case "
                                "where each x is consumed by exactly "
                                "one op. but %s is consumed by %d ops." % (x.name, len(ops)))
    op = ops[0]
    pxg_rule = pxg_registry(op, colocate_gradients_with_ops, gate_gradients)
    x_grad = pxg_rule(x, [grad_dict[z] for z in zs])
    out.append(x_grad)

  return out


class AmortizedGaussianSanitizer(object):
  """Sanitizer with Gaussian noise and amoritzed privacy spending accounting.

  This sanitizes a tensor by first clipping the tensor, summing the
  tensor and then adding appropriate amount of noise. It also uses an
  amortized accountant to keep track of privacy spending.
  """

  def __init__(self, accountant, default_option):
    """Construct an AmortizedGaussianSanitizer.

    Args:
      accountant: the privacy accountant. Expect an amortized one.
      default_option: the default ClipOptoin.
    """

    self._accountant = accountant
    self._default_option = default_option
    self._options = {}

  def set_option(self, tensor_name, option):
    """Set options for an individual tensor.

    Args:
      tensor_name: the name of the tensor.
      option: clip option.
    """

    self._options[tensor_name] = option

  def sanitize(self,
               x,
               eps_delta,
               sigma=None,
               option=ClipOption(None, None),
               tensor_name=None,
               num_examples=None,
               add_noise=True):
    """Sanitize the given tensor. This santize a given tensor by first applying
    l2 norm clipping and then adding Gaussian noise. It calls the privacy
    accountant for updating the privacy spending.

    Args:
      x: the tensor to sanitize.
      eps_delta: a pair of eps, delta for (eps,delta)-DP. Use it to
        compute sigma if sigma is None.
      sigma: if sigma is not None, use sigma.
      option: a ClipOption which, if supplied, used for
        clipping and adding noise.
      tensor_name: the name of the tensor.
      num_examples: if None, use the number of "rows" of x.
      add_noise: if True, then add noise, else just clip.

    Returns:
      a pair of sanitized tensor and the operation to accumulate privacy
      spending.
    """

    if sigma is None:
      eps, delta = eps_delta
      with tf.control_dependencies([
          tf.Assert(tf.greater(eps, 0), ["eps needs to be greater than 0"]),
          tf.Assert(tf.greater(delta, 0), ["delta needs to be greater than 0"])
      ]):
        # The following formula is taken from
        #   Dwork and Roth, The Algorithmic Foundations of Differential
        #   Privacy, Appendix A.
        #   http://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf
        sigma = tf.sqrt(2.0 * tf.log(1.25 / delta)) / eps

    l2norm_bound, clip = option
    if l2norm_bound is None:
      l2norm_bound, clip = self._default_option
      if ((tensor_name is not None) and (tensor_name in self._options)):
        l2norm_bound, clip = self._options[tensor_name]
    if clip:
      x = BatchClipByL2norm(x, l2norm_bound)

    if add_noise:
      if num_examples is None:
        num_examples = tf.slice(tf.shape(x), [0], [1])
      privacy_accum_op = self._accountant.accumulate_privacy_spending(eps_delta, sigma, num_examples)
      with tf.control_dependencies([privacy_accum_op]):
        saned_x = AddGaussianNoise(tf.reduce_sum(x, 0), sigma * l2norm_bound)
    else:
      saned_x = tf.reduce_sum(x, 0)
    return saned_x


class SGDNormMomentum(optimizer.Optimizer):

  def __init__(self, learning_rate=0.001, mu=0.9, norm=10.0, use_locking=False, name="SGDmomentum"):
    super(SGDNormMomentum, self).__init__(use_locking, name)
    self._lr = learning_rate
    self._mu = mu
    self._norm = norm

    self._lr_t = None
    self._mu_t = None
    self._norm_t = None

  def _create_slots(self, var_list):
    for v in var_list:
      self._zeros_slot(v, "a", self._name)
      self._zeros_slot(v, "n", self._name)

  def _apply_dense(self, grad, weight):
    learning_rate_t = tf.cast(self._lr_t, weight.dtype.base_dtype)
    mu_t = tf.cast(self._mu_t, weight.dtype.base_dtype)
    norm_t = tf.cast(self._norm_t, weight.dtype.base_dtype)
    momentum = self.get_slot(weight, "a")
    norm = self.get_slot(weight, "n")

    if momentum.get_shape().ndims == 2:
      momentum_mean = tf.reduce_mean(momentum, axis=1, keep_dims=True)
    elif momentum.get_shape().ndims == 1:
      momentum_mean = momentum
    else:
      momentum_mean = momentum

    norm_update = learning_rate_t / norm + norm
    norm_t = tf.assign(norm_t, norm_update)
    momentum_update = (grad / norm_t) + (mu_t * momentum_mean)
    momentum_t = tf.assign(momentum, momentum_update, use_locking=self._use_locking)

    weight_update = learning_rate_t * momentum_t
    weight_t = tf.assign_sub(weight, weight_update, use_locking=self._use_locking)

    return tf.group(*[weight_t, norm_t, momentum_t])

  def _prepare(self):
    self._lr_t = tf.convert_to_tensor(self._lr, name="learning_rate")
    self._mu_t = tf.convert_to_tensor(self._mu, name="momentum_term")
    self._norm_t = tf.convert_to_tensor(self._norm, name="normalizing_term")


class VariableClippingOptimizer(optimizer.Optimizer):
  """Wrapper optimizer that clips the norm of specified variables after update.

  This optimizer delegates all aspects of gradient calculation and application
  to an underlying optimizer.  After applying gradients, this optimizer then
  clips the variable to have a maximum L2 norm along specified dimensions.
  NB: this is quite different from clipping the norm of the gradients.

  Multiple instances of `VariableClippingOptimizer` may be chained to specify
  different max norms for different subsets of variables.

  This is more efficient at serving-time than using normalization during
  embedding lookup, at the expense of more expensive training and fewer
  guarantees about the norms.

  @@__init__
  """

  def __init__(self,
               opt,
               vars_to_clip_dims,
               max_norm,
               use_locking=False,
               colocate_clip_ops_with_vars=False,
               name="VariableClipping"):
    """Construct a new clip-norm optimizer.

    Args:
      opt: The actual optimizer that will be used to compute and apply the
        gradients. Must be one of the Optimizer classes.
      vars_to_clip_dims: A dict with keys as Variables and values as lists
        of dimensions along which to compute the L2-norm.  See
        `tf.clip_by_norm` for more details.
      max_norm: The L2-norm to clip to, for all variables specified.
      use_locking: If `True` use locks for clip update operations.
      colocate_clip_ops_with_vars: If `True`, try colocating the clip norm
        ops with the corresponding variable.
      name: Optional name prefix for the operations created when applying
        gradients.  Defaults to "VariableClipping".
    """
    super(VariableClippingOptimizer, self).__init__(use_locking, name)
    self._opt = opt
    # Defensive copy of input dict
    self._vars_to_clip_dims = {var: clip_dims[:] for var, clip_dims in vars_to_clip_dims.items()}
    self._max_norm = max_norm
    self._colocate_clip_ops_with_vars = colocate_clip_ops_with_vars

  def compute_gradients(self, *args, **kwargs):
    return self._opt.compute_gradients(*args, **kwargs)

  def get_slot(self, *args, **kwargs):
    return self._opt.get_slot(*args, **kwargs)

  def get_slot_names(self, *args, **kwargs):
    return self._opt.get_slot_names(*args, **kwargs)

  def apply_gradients(self, grads_and_vars, global_step=None, name=None):
    with tf.name_scope(name, self._name) as name:
      update_op = self._opt.apply_gradients(grads_and_vars, global_step=global_step)
      clip_update_ops = []
      with tf.control_dependencies([update_op]):
        for grad, var in grads_and_vars:
          if grad is None or var not in self._vars_to_clip_dims:
            continue
          with tf.name_scope("clip_" + var.op.name):
            if isinstance(grad, tf.Tensor):
              clip_update_ops.append(self._clip_dense(var))
            else:
              clip_update_ops.append(self._clip_sparse(grad, var))

      # In case no var was clipped, still need to run the update_op.
      return tf.group(*([update_op] + clip_update_ops), name=name)

  def _clip_dense(self, var):
    with self._maybe_colocate_with(var):
      updated_var_value = var.read_value()
      normalized_var = tf.clip_by_norm(updated_var_value, self._max_norm,
                                       self._vars_to_clip_dims[var])
      delta = updated_var_value - normalized_var
    with tf.colocate_with(var):
      return var.assign_sub(delta, use_locking=self._use_locking)

  def _clip_sparse(self, grad, var):
    assert isinstance(grad, tf.IndexedSlices)
    clip_dims = self._vars_to_clip_dims[var]
    if 0 in clip_dims:
      log.warn(
          "Clipping norm across dims %s for %s is inefficient "
          "when including sparse dimension 0.", clip_dims, var.op.name)
      return self._clip_dense(var)

    with tf.colocate_with(var):
      var_subset = tf.gather(var, grad.indices)
    with self._maybe_colocate_with(var):
      normalized_var_subset = tf.clip_by_norm(var_subset, self._max_norm, clip_dims)
      delta = tf.IndexedSlices(var_subset - normalized_var_subset, grad.indices, grad.dense_shape)
    with tf.colocate_with(var):
      return var.scatter_sub(delta, use_locking=self._use_locking)

  @contextlib.contextmanager
  def _maybe_colocate_with(self, var):
    """Context to colocate with `var` if `colocate_clip_ops_with_vars`."""
    if self._colocate_clip_ops_with_vars:
      with tf.colocate_with(var):
        yield
    else:
      yield


def _is_all_zeros(grad):
  all_zeros = tf.equal(tf.count_nonzero(grad), 0)
  return all_zeros


def _get_wrapper(fn, opt):

  def wrapper(self, grad, *args, **kwargs):
    all_zeros = _is_all_zeros(grad)

    def call_fn():
      with tf.control_dependencies([fn(grad, *args, **kwargs)]):
        return tf.no_op()

    return tf.cond(all_zeros, tf.no_op, call_fn)

  wrapper = types.MethodType(wrapper, opt)
  return wrapper


class MultitaskOptimizer(object):
  """Optimizer wrapper making all-zero gradients harmless.

  This might be useful when a multi-task loss is used,
  and some components of the loss might be
  not present (e.g. masked out) in some training batches.
  Technically their gradient would be zero,
  which would normally affect the optimizer state
  (e.g. push running average to zero).
  However this is not the desired behaviour,
  since the missing loss component
  should be treated as unknown rather than zero.

  This wrapper filters out all-zero gradient tensors,
  therefore preserving the optimizer state.

  If gradient clipping by global norm is used,
  the provided function clip_gradients_by_global_norm
  should be used (and specified explicitly by the user).
  Otherwise the global norm would be underestimated
  because of all-zero tensors that should be ignored.

  The gradient calculation and application
  are delegated to an underlying optimizer.
  The gradient application is altered only for all-zero tensors.

  Example:
  ```python
  momentum_optimizer = tf.train.MomentumOptimizer(
    learning_rate, momentum=0.9)
  multitask_momentum_optimizer = tefla.core.optimizer.MultitaskOptimizer(
    momentum_optimizer)
  gradvars = multitask_momentum_optimizer.compute_gradients(
    loss)
  gradvars_clipped, _ = tefla.core.optimizer.clip_gradients_by_global_norm(
    gradvars, 15.0)
  train_op = multitask_momentum_optimizer.apply_gradients(
    gradvars_clipped, global_step=batch)
  ```
  """

  def __init__(self, opt):
    """Constructor.

    Args:
      opt: an instance of a class that implements tf.train.Optimizer.
    """
    if not isinstance(opt, optimizer.Optimizer):
      raise TypeError('Supplied optimizer must be an instance of tf.train.Optimizer')
    self._opt = opt
    overridden_methods = ('_apply_dense', '_resource_apply_dense', '_apply_sparse',
                          '_resource_apply_sparse')
    for name in overridden_methods:
      fn = getattr(self._opt, name)
      wrapper = _get_wrapper(fn, self._opt)
      setattr(self._opt, name, wrapper)

  def __getattr__(self, name):
    return getattr(self._opt, name)


def clip_gradients_by_global_norm(gradients_variables, clip_norm=20.):
  """Clips gradients of a multitask loss by their global norm.

  Ignores all-zero tensors when computing the global norm.

  Args:
    gradients_variables: a list of pairs (gradient, variable).
    clip_norm: a float Tensor, the global norm to clip on. Default is 20.0.

  Returns:
    list: A list of pairs of the same type as gradients_variables,.
    fixed_global_norm: A 0-D (scalar) Tensor representing the global norm.
  """
  gradients, variables = six.moves.zip(*gradients_variables)

  def _replace_nonexisting_grad(grad):
    if grad is None:
      return grad
    all_zeros = _is_all_zeros(grad)
    return tf.cond(all_zeros, lambda: tf.zeros([], dtype=tf.as_dtype(grad.dtype)), lambda: grad)

  nonzero_gradients = [_replace_nonexisting_grad(g) for g in gradients]
  fixed_global_norm = tf.global_norm(nonzero_gradients)
  gradients, _ = tf.clip_by_global_norm(gradients, clip_norm, use_norm=fixed_global_norm)
  return list(six.moves.zip(gradients, variables)), fixed_global_norm


class MovingAverageOptimizer(optimizer.Optimizer):
  """Optimizer that computes a moving average of the variables.

  Empirically it has been found that using the moving average of the trained
  parameters of a deep network is better than using its trained parameters
  directly. This optimizer allows you to compute this moving average and swap
  the variables at save time so that any code outside of the training loop will
  use by default the averaged values instead of the original ones.

  Example of usage:

  ```python

  // Encapsulate your favorite optimizer (here the momentum one)
  // inside the MovingAverageOptimizer.
  opt = tf.train.MomentumOptimizer(learning_rate, FLAGS.momentum)
  opt = tefla.core.optimizer.MovingAverageOptimizer(opt)
  // Then create your model and all its variables.
  model = build_model()
  // Add the training op that optimizes using opt.
  // This needs to be called before swapping_saver().
  opt.minimize(cost, var_list)
  // Then create your saver like this:
  saver = opt.swapping_saver()
  // Pass it to your training loop.
      slim.learning.train(
          model,
          ...
          saver=saver)
  ```

  Note that for evaluation, the normal saver should be used instead of
  swapping_saver().
  """

  def __init__(self, opt, average_decay=0.9999, num_updates=None, sequential_update=True):
    """Construct a new MovingAverageOptimizer.

    Args:
      opt: A tf.Optimizer that will be used to compute and apply gradients.
      average_decay: Float.  Decay to use to maintain the moving averages
                     of trained variables.
                     See tf.train.ExponentialMovingAverage for details.
      num_updates: Optional count of number of updates applied to variables.
                   See tf.train.ExponentialMovingAverage for details.
      sequential_update: Bool. If False, will compute the moving average at the
                         same time as the model is updated, potentially doing
                         benign data races.
                         If True, will update the moving average after gradient
                         updates.
    """
    self._optimizer = opt
    self._ema = tf.train.ExponentialMovingAverage(average_decay, num_updates=num_updates)
    self._variable_map = None
    self._sequential_update = sequential_update

  def compute_gradients(self, *args, **kwargs):
    return self._optimizer.compute_gradients(*args, **kwargs)

  def apply_gradients(self, grads_and_vars, global_step=None, name=None):
    train_op = self._optimizer.apply_gradients(grads_and_vars, global_step=global_step, name=name)
    var_list = [x[1] for x in grads_and_vars if x[0] is not None]
    self._variable_map = {}
    if self._sequential_update:
      with tf.control_dependencies([train_op]):
        ma_op = self._ema.apply(var_list)
    else:
      ma_op = self._ema.apply(var_list)

    for v in var_list:
      v_avg = self._ema.average(v)
      self._variable_map[v.op.name] = v_avg
      self._variable_map[v_avg.op.name] = v
    return tf.group(train_op, ma_op, name="train_with_avg")

  def swapping_saver(self, var_list=None, name='swapping_saver', **kwargs):
    """Create a saver swapping moving averages and variables.

    You should use this saver during training.  It will save the moving averages
    of the trained parameters under the original parameter names.  For
    evaluations or inference you should use a regular saver and it will
    automatically use the moving averages for the trained variable.

    You must call this function after all variables have been created and after
    you have called Optimizer.minimize().

    Args:
      var_list: List of variables to save, as per `Saver()`.
                If set to None, will save all the variables that have been
                created before this call.
      name: The name of the saver.
      **kwargs: Keyword arguments of `Saver()`.

    Returns:
      A `tf.train.Saver` object.

    Raises:
      RuntimeError: If apply_gradients or minimize has not been called before.
    """

    if self._variable_map is None:
      raise RuntimeError('Must call apply_gradients or minimize before '
                         'creating the swapping_saver')
    if var_list is None:
      var_list = tf.global_variables()
    if not isinstance(var_list, dict):
      var_list = saver.BaseSaverBuilder.OpListToDict(var_list)
    # Now swap variables and moving averages
    swapped_var_list = {}
    for k, v in six.iteritems(var_list):
      v_swap = self._variable_map.get(v.op.name, None)
      if v_swap:
        swapped_var_list[k] = v_swap
      else:
        swapped_var_list[k] = v
    # Build the swapping saver.
    return saver.Saver(swapped_var_list, name=name, **kwargs)


class NadamOptimizer(tf.train.AdamOptimizer):
  """Optimizer that implements the Nadam algorithm.

  See [Dozat, T., 2015](http://cs229.stanford.edu/proj2015/054_report.pdf).
  """

  def _apply_dense(self, grad, var):
    m = self.get_slot(var, "m")
    v = self.get_slot(var, "v")
    beta1_power, beta2_power = self._get_beta_accumulators()
    return training_ops.apply_adam(
        var,
        m,
        v,
        tf.cast(beta1_power, var.dtype.base_dtype),
        tf.cast(beta2_power, var.dtype.base_dtype),
        tf.cast(self._lr_t, var.dtype.base_dtype),
        tf.cast(self._beta1_t, var.dtype.base_dtype),
        tf.cast(self._beta2_t, var.dtype.base_dtype),
        tf.cast(self._epsilon_t, var.dtype.base_dtype),
        grad,
        use_locking=self._use_locking,
        use_nesterov=True).op

  def _resource_apply_dense(self, grad, var):
    m = self.get_slot(var, "m")
    v = self.get_slot(var, "v")
    beta1_power, beta2_power = self._get_beta_accumulators()
    return training_ops.resource_apply_adam(
        var.handle,
        m.handle,
        v.handle,
        tf.cast(beta1_power, grad.dtype.base_dtype),
        tf.cast(beta2_power, grad.dtype.base_dtype),
        tf.cast(self._lr_t, grad.dtype.base_dtype),
        tf.cast(self._beta1_t, grad.dtype.base_dtype),
        tf.cast(self._beta2_t, grad.dtype.base_dtype),
        tf.cast(self._epsilon_t, grad.dtype.base_dtype),
        grad,
        use_locking=self._use_locking,
        use_nesterov=True)

  def _apply_sparse_shared(self, grad, var, indices, scatter_add):
    beta1_power, beta2_power = self._get_beta_accumulators()
    beta1_power = tf.cast(beta1_power, var.dtype.base_dtype)
    beta2_power = tf.cast(beta2_power, var.dtype.base_dtype)
    lr_t = tf.cast(self._lr_t, var.dtype.base_dtype)
    beta1_t = tf.cast(self._beta1_t, var.dtype.base_dtype)
    beta2_t = tf.cast(self._beta2_t, var.dtype.base_dtype)
    epsilon_t = tf.cast(self._epsilon_t, var.dtype.base_dtype)
    lr = (lr_t * tf.sqrt(1 - beta2_power) / (1 - beta1_power))
    # m_t = beta1 * m + (1 - beta1) * g_t
    m = self.get_slot(var, "m")
    m_scaled_g_values = grad * (1 - beta1_t)
    m_t = tf.assign(m, m * beta1_t, use_locking=self._use_locking)
    with tf.control_dependencies([m_t]):
      m_t = scatter_add(m, indices, m_scaled_g_values)
      # m_bar = (1 - beta1) * g_t + beta1 * m_t
      m_bar = m_scaled_g_values + beta1_t * m_t
    # v_t = beta2 * v + (1 - beta2) * (g_t * g_t)
    v = self.get_slot(var, "v")
    v_scaled_g_values = (grad * grad) * (1 - beta2_t)
    v_t = tf.assign(v, v * beta2_t, use_locking=self._use_locking)
    with tf.control_dependencies([v_t]):
      v_t = scatter_add(v, indices, v_scaled_g_values)
    v_sqrt = tf.sqrt(v_t)
    var_update = tf.assign_sub(var, lr * m_bar / (v_sqrt + epsilon_t), use_locking=self._use_locking)
    return tf.group(*[var_update, m_bar, v_t])


class LazyAdamOptimizer(tf.train.AdamOptimizer):
  """Variant of the Adam optimizer that handles sparse updates more
  efficiently.

  The original Adam algorithm maintains two moving-average accumulators
  for each trainable variable; the accumulators are updated at every
  step. This class provides lazier handling of gradient updates for
  sparse variables. It only updates moving-average accumulators for
  sparse variable indices that appear in the current batch, rather than
  updating the accumulators for all indices. Compared with the original
  Adam optimizer, it can provide large improvements in model training
  throughput for some applications. However, it provides slightly
  different semantics than the original Adam algorithm, and may lead to
  different empirical results.
  """

  def _apply_sparse(self, grad, var):
    beta1_power, beta2_power = self._get_beta_accumulators()
    beta1_power = tf.cast(beta1_power, var.dtype.base_dtype)
    beta2_power = tf.cast(beta2_power, var.dtype.base_dtype)
    lr_t = tf.cast(self._lr_t, var.dtype.base_dtype)
    beta1_t = tf.cast(self._beta1_t, var.dtype.base_dtype)
    beta2_t = tf.cast(self._beta2_t, var.dtype.base_dtype)
    epsilon_t = tf.cast(self._epsilon_t, var.dtype.base_dtype)
    lr = (lr_t * tf.sqrt(1 - beta2_power) / (1 - beta1_power))

    # m := beta1 * m + (1 - beta1) * g_t
    m = self.get_slot(var, "m")
    m_t = tf.scatter_update(
        m,
        grad.indices,
        beta1_t * tf.gather(m, grad.indices) + (1 - beta1_t) * grad.values,
        use_locking=self._use_locking)

    # v := beta2 * v + (1 - beta2) * (g_t * g_t)
    v = self.get_slot(var, "v")
    v_t = tf.scatter_update(
        v,
        grad.indices,
        beta2_t * tf.gather(v, grad.indices) + (1 - beta2_t) * tf.square(grad.values),
        use_locking=self._use_locking)

    # variable -= learning_rate * m_t / (epsilon_t + sqrt(v_t))
    m_t_slice = tf.gather(m_t, grad.indices)
    v_t_slice = tf.gather(v_t, grad.indices)
    denominator_slice = tf.sqrt(v_t_slice) + epsilon_t
    var_update = tf.scatter_sub(
        var, grad.indices, lr * m_t_slice / denominator_slice, use_locking=self._use_locking)
    return tf.group(var_update, m_t, v_t)


class ModelAverageCustomGetter(object):
  """Custom_getter class is used to do:
    1. Change trainable variables to local collection and place them at worker
      device
    2. Generate global variables
      Notice that the class should be used with tf.replica_device_setter,
      so that the global center variables and global step variable can be placed
      at ps device. Besides, use 'tf.get_variable' instead of 'tf.Variable' to
      use this custom getter.

    For example,
    ma_custom_getter = ModelAverageCustomGetter(worker_device)
    with tf.device(
      tf.train.replica_device_setter(
        worker_device=worker_device,
        ps_device="/job:ps/cpu:0",
        cluster=cluster)),
      tf.variable_scope('',custom_getter=ma_custom_getter):
      hid_w = tf.get_variable(
        initializer=tf.truncated_normal(
            [IMAGE_PIXELS * IMAGE_PIXELS, FLAGS.hidden_units],
            stddev=1.0 / IMAGE_PIXELS),
        name="hid_w")
      hid_b = tf.get_variable(initializer=tf.zeros([FLAGS.hidden_units]),
                              name="hid_b")
    """

  def __init__(self, worker_device):
    """Create a new `ElasticAverageCustomGetter`.

    Args:
      worker_device: String.  Name of the `worker` job.
    """
    self._worker_device = worker_device
    self._local_2_global = {}

  def __call__(self, getter, name, trainable, collections, *args, **kwargs):
    if trainable:
      with tf.device(self._worker_device):
        local_var = getter(
            name, trainable=True, collections=[tf.GraphKeys.LOCAL_VARIABLES], *args, **kwargs)

      global_variable = tf.Variable(
          name='%s/%s' % (GLOBAL_VARIABLE_NAME, name),
          initial_value=local_var.initialized_value(),
          trainable=False,
          collections=[tf.GraphKeys.GLOBAL_VARIABLES])

      self._local_2_global[local_var] = global_variable
      return local_var
    else:
      return getter(name, trainable, collections, *args, **kwargs)


class ModelAverageOptimizer(optimizer.Optimizer):
  """Wrapper optimizer that implements the Model Average algorithm.

  This is a sync optimizer. During the training, each worker will update
  the local variables and maintains its own local_step, which starts
  from 0 and is incremented by 1 after each update of local variables.
  Whenever the interval_steps divides the local step, the local
  variables from all the workers will be averaged and assigned to global
  center variables. Then the local variables will be assigned by global
  center variables.
  """

  def __init__(self,
               opt,
               num_worker,
               is_chief,
               ma_custom_getter,
               interval_steps=100,
               use_locking=True,
               name="ModelAverageOptimizer"):
    """Construct a new model average optimizer.

    Args:
      opt: The actual optimizer that will be used to update local variables
      num_worker: The number of workers
      is_chief: whether chief worker
      ma_custom_getter: ModelAverageCustomGetter
      interval_steps: An int point value to controls the frequency of the
        average of local variables
      use_locking: If True use locks for update operations
      name: string. Optional name of the returned operation
    """
    super(ModelAverageOptimizer, self).__init__(use_locking, name)
    self._opt = opt
    self._num_worker = num_worker
    self._is_chief = is_chief
    self._local_2_global = ma_custom_getter._local_2_global
    self._interval_steps = interval_steps
    self._accumulator_list = []
    self._chief_init_op = None

    self._local_step = tf.get_variable(
        initializer=0,
        trainable=False,
        collections=[tf.GraphKeys.LOCAL_VARIABLES],
        name="local_step")

    self._opt._prepare()

  def compute_gradients(self, *args, **kwargs):
    """Compute gradients of "loss" for the variables in "var_list".

    This simply wraps the compute_gradients() from the real optimizer.

    Args:
      *args: Arguments for compute_gradients().
      **kwargs: Keyword arguments for compute_gradients().

    Returns:
      A list of (gradient, variable) pairs.
    """
    return self._opt.compute_gradients(*args, **kwargs)

  def _local_vars_update(self, var_list):
    """Get the update ops for the local variables in "var_list".

    Args:
      var_list: Optional list or tuple of 'tf.Variable' to update

    Returns:
      An update op
    """
    if not var_list:
      raise ValueError('The list of local_variables should not be empty')
    update_ops = []
    global_center_vars = [self._local_2_global[var] for var in var_list]
    for lvar, gvar in zip(var_list, global_center_vars):
      with tf.device(lvar.device):
        update_ops.append(tf.assign(lvar, gvar.read_value()))
    return tf.group(*(update_ops))

  def apply_gradients(self, grads_and_vars, global_step=None, name=None):
    """Apply gradients to variables.

    This contains most of the synchronization implementation and also wraps the
    apply_gradients() from the real optimizer. The chief work updates global
    variables.

    Args:
      grads_and_vars: List of (gradient, variable) pairs as returned by
        compute_gradients().
      global_step: Optional Variable to increment by one after the
        variables have been updated.
      name: Optional name for the returned operation.  Default to the
        name passed to the Optimizer constructor.

    Returns:
      A conditional 'Operation' that update both local and global variables or
      just local variables

    Raises:
      ValueError: If the grads_and_vars is empty.
      ValueError: If global step is not provided, the staleness cannot be
        checked.
    """

    # update local variables
    if not grads_and_vars:
      raise ValueError("Must supply at least one variable")
    if global_step is None:
      raise ValueError("Global step is required")

    apply_updates = self._opt.apply_gradients(grads_and_vars)
    with tf.control_dependencies([apply_updates]):
      local_update = tf.assign_add(self._local_step, 1, name='local_step_update').op

    # update global variables.
    def _Update_global_variables():
      local_vars = [v for g, v in grads_and_vars if g is not None]
      global_vars = [self._local_2_global[v] for v in local_vars]
      # sync queue
      with tf.colocate_with(global_step):
        sync_queue = tf.FIFOQueue(-1, [tf.bool], shapes=[[]], shared_name='sync_queue')
      train_ops = []
      aggregated_vars = []
      with tf.name_scope(None, self._name + '/global'):
        for var, gvar in zip(local_vars, global_vars):
          with tf.device(gvar.device):
            if isinstance(var._ref(), tf.Tensor):
              var_accum = tf.ConditionalAccumulator(
                  var.dtype, shape=var.get_shape(), shared_name=gvar.name + "/var_accum")
              train_ops.append(var_accum.apply_grad(var._ref(), local_step=global_step))
              aggregated_vars.append(var_accum.take_grad(self._num_worker))
            else:
              raise ValueError("Unknown local variable type!")
            self._accumulator_list.append((var_accum, gvar.device))
      # chief worker updates global vars and enqueues tokens to the sync queue
      if self._is_chief:
        update_ops = []
        with tf.control_dependencies(train_ops):
          for avg_var, gvar in zip(aggregated_vars, global_vars):
            with tf.device(gvar.device):
              update_ops.append(tf.assign(gvar, avg_var))
          with tf.device(global_step.device):
            update_ops.append(tf.assign_add(global_step, 1))
        with tf.control_dependencies(update_ops), tf.device(global_step.device):
          tokens = tf.fill([self._num_worker - 1], tf.constant(False))
          sync_op = sync_queue.enqueue_many(tokens)
      else:
        with tf.control_dependencies(train_ops), tf.device(global_step.device):
          sync_op = sync_queue.dequeue()

      with tf.control_dependencies([sync_op]):
        local_update_op = self._local_vars_update(local_vars)
      return local_update_op

    with tf.control_dependencies([local_update]):
      condition = tf.equal(tf.mod(self._local_step, self._interval_steps), 0)
      conditional_update = tf.cond(condition, _Update_global_variables, tf.no_op)

    chief_init_ops = []
    for accum, dev in self._accumulator_list:
      with tf.device(dev):
        chief_init_ops.append(accum.set_global_step(global_step, name="SetGlobalStep"))
    self._chief_init_op = tf.group(*(chief_init_ops))

    return conditional_update

  def get_init_op(self):
    """Returns the op to let all the local variables equal to the global
    variables before the training begins."""
    return self._local_vars_update(tf.trainable_variables())

  def make_session_run_hook(self):
    """Creates a hook to handle ModelAverage ops such as initialization."""
    return _ModelAverageOptimizerHook(self, self._is_chief)


class _ModelAverageOptimizerHook(tf.train.SessionRunHook):

  def __init__(self, ma_optimizer, is_chief):
    """Creates hook to handle ModelAverageOptimizer initialization ops.

    Args:
      ea_optimizer: `ModelAverageOptimizer` which this hook will initialize.
      is_chief: `Bool`, whether is this a chief replica or not.
    """
    self._ma_optimizer = ma_optimizer
    self._is_chief = is_chief

  def begin(self):
    self._local_init_op = tf.local_variables_initializer()
    self._global_init_op = None
    if self._is_chief:
      self._global_init_op = tf.global_variables_initializer()
      self._chief_init_op = self._ma_optimizer._chief_init_op
    self._variable_init_op = self._ma_optimizer.get_init_op()
