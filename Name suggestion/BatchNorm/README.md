This model adds Batch Normalization and kaiming init for the previous model. Explained more <a href="https://www.youtube.com/watch?v=P6sfmUTpUmc&t=3004s">Here</a>
## About Model
When working with activation functions like tanh and ReLU, if the weights aren't properly controlled, some neurons may become inactive or dead, causing them not to update parameters with gradients effectively. One simple explanation for this phenomenon is that with tanh as the activation function, when the input is more than 1 or less than -1, the gradients will be zero (derivative equals zero). Additionally, if the gradients are close to 0 within the tanh function, the parameters will pass through without being updated. To mitigate this issue, we aim to normalize the weights during initialization before feeding them into the network.<br />

<a href="https://arxiv.org/abs/1502.01852">Kaiming</a> initialization is one solution that utilizes standard deviation and mean to normalize parameters. It incorporates a gain value and fan mode. The gain value varies depending on the activation functions used, and the fan mode determines whether to consider the input value of the layer (fan_in) or the output value (fan_out).<br />

For example the below function is used for the tanh's kaiming init:

$$
\text{Kaiming initialization for tanh (normal)} : \quad \text{std} = \text{gain} \times \sqrt{\frac{1}{\text{fan\_in}}}
$$

For tanh the gain is 5/3.
For more info check out pytorch's <a href="https://pytorch.org/docs/stable/nn.init.html#torch.nn.init.kaiming_normal_">docs</a>

As our model grows larger and more complex, the previous methods used for normalization during initialization can become unstable, akin to balancing a pen on your finger. To address this challenge, we employ Batch Normalization instead.

Batch Normalization operates by normalizing the neurons within layers. It computes the mean and standard deviation of each batch and adjusts the values accordingly. Additionally, it incorporates parameters for scaling and shifting, known as gain and bias.

$$
\hat{x}_i = \frac{x_i - \mu}{\sqrt{\sigma^2 + \epsilon}}
$$

$$
y_i = \gamma \hat{x}_i + \beta
$$

Where:
- \( x_i \) is the input to the layer.
- \( \mu \) is the mean of the mini-batch.
- \( \sigma \) is the standard deviation of the mini-batch.
- \( \epsilon \) is a small constant (usually added for numerical stability).
- \( \hat{x}_i \) is the normalized input.
- \( \gamma \) and \( \beta \) are learnable parameters (scale and shift, respectively).
- \( y_i \) is the output after normalization and scaling.

For more info check out pytorch's <a href="https://pytorch.org/docs/stable/generated/torch.nn.BatchNorm1d.html#torch.nn.BatchNorm1d">docs</a>.


One drawback of Batch Normalization is its susceptibility to coupling samples, which can lead to slight variations in entropy across samples.


