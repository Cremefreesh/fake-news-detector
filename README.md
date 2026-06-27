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
