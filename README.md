AI Fake News Detection Chrome Extension -
A Chrome extension that analyses social media posts and news articles in real time.

Using a custom PyTorch fake-news classifier. 
Developed a FastAPI backend for model inference, integrated LLM-generated explanations for interpretability, 
and built a React/JavaScript frontend for browser deployment. 
Evaluated model performance using accuracy, precision, recall and F1-score, 
and packaged the project using Chrome Manifest V3.

Chrome Extension 
      |
      ->   React Frontend 
                |
    ---------------FASTapi Backend--------------------
    |                         |                      |
Pytorch Classifier     Embedding Search      LLM Explanation
    |                         |                      |
    |                         |                      |
    --------------->    Final Prediction     <--------



Raw Dataset
      │
Cleaning
      │
Tokenization
      │
Vocabulary
      │
PyTorch Dataset
      │
Neural Network
      │
Training
      │
Evaluation
      │
Saved Model (.pt)



I built the preprocessing pipeline, trained the model in PyTorch, evaluated it with precision, recall, F1-score, and deployed it behind a FastAPI API.


Collect data
↓
Understand data
↓
Clean data
↓
Explore data
↓
Split data
↓
Engineer features
↓
Train model
