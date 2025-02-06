# g-eval_persona-chat
Questo progetto applica il framework G-Eval, descritto nel relativo paper, al dataset PersonaChat per valutare la qualità delle risposte in contesti conversazionali. Utilizzando GPT‑4 tramite Azure Open AI Services, il sistema genera due tipi di valutazioni per ciascuna risposta: una valutazione numerica (con venti iterazioni per garantire robustezza) e una valutazione argomentata che spiega i motivi alla base del punteggio assegnato. I risultati delle valutazioni automatiche vengono confrontati con i giudizi umani, permettendo di calcolare diverse metriche di correlazione (Pearson, Spearman, Cohen, Tau) per analizzare l'affidabilità del metodo.

Lo script **gpt4_eval_persona_chat.py** contiene la logica utilizzata per la generazione delle risposte tramite chiamata API su Azure OpenAI Services.

Mentre il notebook **data_explorer.ipynb** contiene la logica per la visualizzazione e la valutazione, tramite analisi di correlazione, dei risultati ottenuti