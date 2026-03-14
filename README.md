# 🎮 Engine 2D - Estudo de Mecânicas com Pygame

Este é um projeto desenvolvido do zero utilizando **Python** e a biblioteca **Pygame**. O objetivo principal foi construir as fundações e mecânicas lógicas de uma *engine* 2D (Top-Down) sem depender de ferramentas prontas (como Unity ou Godot), focando-se na resolução de problemas e arquitetura de código.

## 🚀 Mecânicas Desenvolvidas

* **Física e Inércia:** Implementação de vetores de velocidade e aceleração para simular o atrito e criar uma movimentação fluida do personagem.
* **Máquina de Estados de Animação:** Sistema dinâmico que altera os *sprites* em tempo real com base na direção do movimento (16 direções) e na ação atual (andar, socar, equipar arma, atirar).
* **Sistema de Armas e Inventário:** Lógica de *loot* (recolher itens do chão), gestão de pentes de munição e mecânica de recarga mapeada em eventos de teclado.
* **Controlo de Cooldowns:** Implementação de *ticks* baseados nos quadros do jogo (FPS) para gerenciar a cadência dos disparos e a duração das ações.
* **Arquitetura Modular:** Código refatorado e dividido em múltiplos ficheiros (`main.py`, `player.py`, `weapons.py`, `settings.py`) aplicando os princípios da Programação Orientada a Objetos (POO).

## 🛠️ Tecnologias Utilizadas
* **Python 3**
* **Pygame**

## 🎥 Demonstração
*(Coloque aqui o link do vídeo do LinkedIn ou um GIF do jogo a correr)*

---
*Este projeto faz parte do meu portefólio de estudos para desenvolver uma base sólida em lógica de programação.*