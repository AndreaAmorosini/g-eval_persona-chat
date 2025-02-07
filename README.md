# g-eval_persona-chat
Questo progetto applica il framework G-Eval, descritto nel relativo paper, ai dataset PersonaChat, TopicalChat e Fine-grained Evaluation of Dialogue per valutare la qualità delle risposte in contesti conversazionali. Utilizzando GPT‑4 tramite Azure Open AI Services, il sistema genera due tipi di valutazioni per ciascuna risposta: una valutazione numerica (con venti iterazioni per garantire robustezza) e una valutazione argomentata che spiega i motivi alla base del punteggio assegnato. I risultati delle valutazioni automatiche vengono confrontati con i giudizi umani, permettendo di calcolare diverse metriche di correlazione (Pearson, Spearman, Cohen, Tau) per analizzare l'affidabilità del metodo.

Lo script **gpt4_eval_persona_chat.py** contiene la logica utilizzata per la generazione delle risposte tramite chiamata API su Azure OpenAI Services.

Mentre il notebook **data_explorer.ipynb** contiene la logica per la visualizzazione e la valutazione, tramite analisi di correlazione, dei risultati ottenuti

I risultati con le 20 valutazioni per risposta da PersonaChat sono disponibili all'interno del file [evaluations_pc.json](./results/evaluations_pc.json).

Mentre i risultati giustificati con spiegazione sono disponibili all'interno del file [evaluations_justified.json](./results/evaluations_justified.json).

I risultati generati da TopicalChat sono disponibili all'interno del file [evaluations_tc_usr_data.json](./results/evaluations_tc_usr_data.json).

I risultati generati da Fine-grained Evaluation of Dialogue sono disponibili all'interno del file [evaluations_fed_data.json](./results/evaluations_fed_data.json).

## Installazione:
``` bash
conda env create -f environment.yml
