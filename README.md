# GOTTA - Quiz sobre Drones & Queimadas

## O que faz

Uma página interativa no site do projeto de drone que apresenta um quiz educativo para usuários. O usuário inicia um quiz, responde às perguntas (múltipla escolha, verdadeiro/falso etc.), recebe feedback imediato e uma pontuação final. 

## Problema que resolve

Aumenta o engajamento e a conscientização sobre prevenção de queimadas e uso de drones em monitoramento ambiental, transformando conteúdo técnico em atividade interativa e avaliável.


## PASSO A PASSO DE COMO RODAR O PROJETO

1. Baixe o Python.

2. No cmd, dentro da pasta Quiz, cole esse código:

pip install -r requirements.txt

3. Depois, cole esse código: uvicorn main:app --reload

4. Caso o site não rode, cole isso no cmd:

python -m uvicorn main:app --reload
