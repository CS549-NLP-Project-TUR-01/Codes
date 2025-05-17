"""
    
You are an expert AI developer and NLP engineer. I’m working on a Turkish game‑review sentiment‑analysis project. I’ve already completed data loading, Turkish‑specific preprocessing (lowercasing, punctuation removal, stop‑word filtering, Zemberek lemmatization), and train/val/test splits. I now need you to:

1. **Audit Completed Steps**  
   a. Verify that my current preprocessing, splitting, and vectorization pipelines are complete and optimal for Turkish text.  
   b. Point out any missing or redundant transformations.  

2. **Refine Model Setup**  
   a. Suggest improvements to TF‑IDF and averaged embeddings for SVM/Logistic Regression.  
   b. Recommend best practices for fine‑tuning BERTurk or multilingual BERT (mBERT) on Turkish: learning rates, batch sizes, scheduler strategies, hardware utilization.  

3. **Hyperparameter & Validation Strategy**  
   a. Propose a concrete hyperparameter search space and strategy (GridSearchCV, Bayesian optimization, etc.) for both classical and transformer models.  
   b. Define validation protocols to guard against overfitting (e.g., k‑fold CV, early stopping criteria, metric thresholds).

4. **Evaluation & Reporting**  
   a. Confirm which metrics are most informative (accuracy, per‑class precision/recall/F1, confusion matrix, ROC/AUC) given class balance.  
   b. Provide code snippets to generate and visualize these metrics.  
   c. Recommend how to present results in a reproducible report (e.g., Jupyter notebook sections, logging with MLflow).

5. **Next Steps & Timeline**  
   a. Outline the minimal viable experimental plan: which model(s) to train first, time estimates, resource requirements.  
   b. Flag any risks or data‑quality issues that could derail progress, and suggest mitigation.

**Context & Resources**  
- Dataset: ~10,000 Turkish game reviews, labeled positive/negative/neutral.  
- Environment: Python 3.10, scikit‑learn, Hugging Face Transformers, Zemberek, GPU server available.  
- Deliverables:  
  1. Cleaned, reproducible preprocessing pipeline  
  2. Trained baseline SVM/LR and BERTurk models with hyperparameter logs  
  3. Final evaluation report (notebook + PDF slides)

Use concise bullet points, reference code examples in Python, and clearly mark any assumptions you make. Let’s iterate step‑by‑step to reach a robust, production‑ready sentiment classifier for Turkish game reviews.

"""