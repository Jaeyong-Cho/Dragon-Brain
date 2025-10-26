# Deep Learning and Neural Networks

Deep learning uses artificial neural networks with multiple layers to learn complex patterns.

## Neural Network Basics

### Artificial Neuron

Mimics biological neurons:

- **Inputs**: Features from data
- **Weights**: Learnable parameters
- **Activation Function**: Non-linear transformation
- **Output**: Prediction or signal

### Activation Functions

- **ReLU** (Rectified Linear Unit): Most common
- **Sigmoid**: Output between 0 and 1
- **Tanh**: Output between -1 and 1
- **Softmax**: Multi-class probabilities
- **Leaky ReLU**: Prevents dying neurons

## Neural Network Architectures

### Feedforward Neural Networks

Simple architecture with layers flowing forward:

```python
import torch.nn as nn

class SimpleNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 128)
        self.fc2 = nn.Linear(128, 10)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x
```

### Convolutional Neural Networks (CNN)

Specialized for **image data**:

#### Key Components

- **Convolutional Layers**: Feature extraction
- **Pooling Layers**: Dimensionality reduction
- **Fully Connected Layers**: Classification

#### Popular Architectures

- **LeNet**: Early CNN
- **AlexNet**: ImageNet winner 2012
- **VGG**: Very deep networks
- **ResNet**: Skip connections
- **EfficientNet**: Optimized architecture

### Recurrent Neural Networks (RNN)

Handle **sequential data**:

- LSTM (Long Short-Term Memory)
- GRU (Gated Recurrent Unit)
- Bidirectional RNN

**Applications:**
- Natural Language Processing
- Time series prediction
- Speech recognition

### Transformers

Modern architecture for **NLP tasks**:

- **Self-Attention Mechanism**
- Parallel processing
- State-of-the-art performance

**Notable Models:**
- BERT: Bidirectional understanding
- GPT: Generative pre-training
- T5: Text-to-text framework

## Training Deep Networks

### Backpropagation

Algorithm to compute gradients:

1. **Forward Pass**: Calculate predictions
2. **Loss Calculation**: Measure error
3. **Backward Pass**: Compute gradients
4. **Update Weights**: Optimize parameters

### Optimization Algorithms

- **SGD** (Stochastic Gradient Descent)
- **Adam**: Adaptive learning rates
- **RMSprop**: Root mean square propagation
- **AdaGrad**: Adaptive gradient

### Learning Rate Scheduling

- Step decay
- Exponential decay
- **Cosine annealing**
- Warm-up strategies

## Regularization Techniques

### Dropout

Randomly **deactivate neurons** during training.

### Batch Normalization

Normalize layer inputs to stabilize training.

### Data Augmentation

Artificially expand training data:

- **Random crops**
- Flips and rotations
- Color jittering
- Mixup and CutMix

## Transfer Learning

Use pre-trained models for new tasks:

1. **Feature Extraction**: Freeze early layers
2. **Fine-tuning**: Train all layers with small learning rate

**Benefits:**
- Less data required
- Faster training
- Better performance

## Computer Vision Applications

- **Image Classification**: Categorize images
- **Object Detection**: Locate objects (YOLO, R-CNN)
- **Semantic Segmentation**: Pixel-wise classification
- **Image Generation**: GANs, Diffusion models
- **Face Recognition**: Identity verification

## Natural Language Processing

- **Text Classification**: Sentiment analysis
- **Named Entity Recognition**: Extract entities
- **Machine Translation**: Language conversion
- **Question Answering**: Retrieve answers
- **Text Generation**: Create new text

## Hardware Acceleration

### GPUs

Graphics Processing Units for parallel computation:

- **NVIDIA CUDA**: Most popular
- Thousands of cores
- High memory bandwidth

### TPUs

Google's Tensor Processing Units:

- Optimized for matrix operations
- Cloud-based access

## Frameworks

- **TensorFlow**: Google's framework
- **PyTorch**: Facebook's framework
- **Keras**: High-level API
- **JAX**: Automatic differentiation
