# 🦖 Jogo Dino (Logisim)

## 🎯 1. Descrição Geral do Objetivo do Projeto
Este projeto implementa o clássico "Jogo do Dinossauro" do Google Chrome utilizando apenas circuitos lógicos digitais. Toda a lógica do jogo, incluindo gráficos, colisões, movimentação e controle de estados, foi desenvolvida diretamente em hardware, sem o uso de linguagens de programação ou motores de jogos.

## 🎓 2. Contexto Acadêmico
O projeto foi desenvolvido como aplicação prática dos conceitos de Arquitetura de Computadores e Sistemas Digitais. Durante sua construção, foram utilizados Máquinas de Estados Finitos (FSM), caminhos de dados (Datapaths), registradores de deslocamento (Shift Registers) e técnicas de modularização de circuitos, demonstrando como conceitos teóricos de hardware podem ser aplicados na criação de um sistema interativo.

## 🛠️ 3. Tecnologias e Ferramentas Utilizadas
- **Simulador:** Logisim
- **Componentes Lógicos Base:** Portas Lógicas (AND, OR, NOT), Multiplexadores, Demultiplexadores.
- **Componentes Sequenciais:** Contadores (Counters), Registradores de Deslocamento (Shift Registers), Flip-Flops.
- **Saída Visual:** DotMatrix (Matriz de LEDs) e Displays BCD (para pontuação).

## 🏗️ 4. Estrutura do Projeto
A arquitetura do projeto foi estruturada de maneira fortemente modular, seguindo boas práticas de design de hardware. O circuito principal (`proba2.circ`) atua como a placa-mãe (top-level) que interliga os diversos barramentos (buses de 16 ou 32 bits) e coordena a comunicação entre os submódulos de clock, processamento de vídeo (sprites), controle de inputs e detecção de colisões.

## ⚙️ 5. Circuitos Implementados e Funcionamento Detalhado

### 🕹️ 5.1. Circuito Principal (Top-Level)
<img width="1067" height="756" alt="Captura de tela 2026-06-03 203239" src="https://github.com/user-attachments/assets/3a54bc44-4ec6-4077-a9a9-8e0753424e14" />

- **Descrição Resumida:** Atua como a placa-mãe do sistema, integrando todos os sub-circuitos e roteando as informações para a Display Matrix.
- **Funcionamento Interno:** Os dados das posições do cacto, do pássaro e do dinossauro convergem para uma série de portas lógicas (ORs) antes de alimentar a Matriz de LEDs. Isso garante que se dois sprites ocuparem o mesmo espaço visual, o pixel correspondente acenda (sobreposição gráfica).
- **Entradas e Saídas:**
  - *Entradas:* Sinal de Clock global, Input do usuário (botão de pulo).
  - *Saídas:* Barramentos conectados à Matriz de LEDs e aos Displays BCD.

### ⏱️ 5.2. Gerador de Clock (`clock zmiana.circ`)
<img width="681" height="445" alt="Captura de tela 2026-06-03 204132" src="https://github.com/user-attachments/assets/296c6a52-571f-43c1-966d-2419a1cd5925" />

- **Descrição Resumida:** Dita o ritmo do jogo e aumenta a dificuldade (velocidade) com o passar do tempo.
- **Funcionamento Interno:** Utiliza contadores para registrar o tempo de jogo. Ao atingir determinados limites (thresholds), a frequência do sinal de clock distribuído para os registradores de deslocamento é aumentada, acelerando os obstáculos.

### 🏃 5.3. Controlador do Personagem (`dinozaur wyswietlanie.circ`)
<img width="1480" height="885" alt="image" src="https://github.com/user-attachments/assets/7a0ff08e-dd0c-48a7-85a5-c06340ccea33" />

- **Descrição Resumida:** Processa os frames do dinossauro (correndo, pulando e parado).
- **Funcionamento Interno:** Durante a corrida, demultiplexadores alternam os sprites das pernas. Ao receber o comando de pulo, a animação de correr recebe um override (ficando fixa). Um contador calibrado atua no eixo Y: incrementando a posição na subida, atingindo um limite máximo num comparador, e revertendo a contagem para a queda.
- **Entradas e Saídas:**
  - *Entradas:* Sinal de pulo (botão), clock.
  - *Saídas:* Barramento com a máscara de pixels atual do dinossauro.

### 🌵 5.4. Módulo de Geração de Obstáculos (`kaktus wyswietlanie.circ` / `mały_lub_duży.circ`)
<img width="1310" height="779" alt="image" src="https://github.com/user-attachments/assets/90b96db5-44a9-4d8b-890f-d08c174e6696" /> <img width="748" height="226" alt="image" src="https://github.com/user-attachments/assets/4f5764a5-f2d8-4067-b89b-8ff902a06b24" />

- **Descrição Resumida:** Gera e desloca os obstáculos terrestres (cactos) e aéreos (pássaros) pela tela.
- **Funcionamento Interno:** Utiliza o componente Random nativo do Logisim para gerar um bit (0 ou 1) que atua como seletor de um MUX, decidindo entre um cacto grande ou pequeno. Contadores definem o *cooldown* entre spawns, garantindo espaço físico e computacional para o pulo. O movimento é feito via Shift Registers (deslocadores) da direita para a esquerda.

### 💥 5.5. Módulo de Colisão (`przegrana.circ`)
<img width="1484" height="908" alt="image" src="https://github.com/user-attachments/assets/fae05cac-af1b-49e8-a6cb-7ebb51d37674" />

- **Descrição Resumida:** Detecta impacto entre o dinossauro e obstáculos.
- **Funcionamento Interno:** Compara o barramento de coordenadas do dinossauro com o dos obstáculos simultaneamente usando uma densa árvore de portas AND. Se um pixel `(X,Y)` do dinossauro e do obstáculo tiverem valor 1 ao mesmo tempo, a porta AND resulta em 1, alimentando uma grande porta OR em cascata que emite o sinal de *Stop*.
- **Entradas e Saídas:**
  - *Entradas:* Coordenadas do Dinossauro, Coordenadas dos Obstáculos.
  - *Saídas:* Sinal de Stop / Game Over.

### 💯 5.6. Módulo de Pontuação (`wynik wyświetlanie.circ`)
<img width="1470" height="825" alt="image" src="https://github.com/user-attachments/assets/cf899390-692e-40db-9a7b-59e76494ee98" /> 

- **Descrição Resumida:** Registra a pontuação do jogo.
- **Funcionamento Interno:** Contadores operam em sincronia com o clock global. Seus valores binários são decodificados para alimentar displays BCD de 7 segmentos.

## 🔄 6. Fluxo de Funcionamento do Sistema Completo (FSM)
O jogo opera como uma Máquina de Estados Finita (FSM) com as seguintes condições:
1. **Estado 0 (Idle/Reset):** O sistema aguarda o pulso inicial. O dinossauro fica na posição base e o contador é zero.
2. **Estado 1 (Running):** O clock global pulsa os sub-circuitos. O dinossauro alterna os frames das pernas e os obstáculos são shiftados da direita para a esquerda.
3. **Estado 2 (Jumping):** Disparado pelo input. A animação das pernas é suspensa e o offset vertical do sprite do dinossauro muda através do contador up/down.
4. **Estado 3 (Game Over):** Acionado pelo sinal de *Stop* do módulo de colisão. O clock do datapath é desativado via uma porta AND negada, congelando o cenário e a pontuação.

## ▶️ 7. Como Executar ou Simular o Projeto
1. Instale o simulador [Logisim](http://www.cburch.com/logisim/) (ou Logisim-Evolution, dependendo da versão utilizada).
2. Clone este repositório.
3. Abra o arquivo principal do projeto (`proba2.circ`) no Logisim.
4. Habilite a simulação de ticks do clock pressionando `Ctrl + K`.
5. Utilize a ferramenta de "Mãozinha" (Poke Tool) ou o mapeamento de teclado configurado para acionar o botão de pulo (Input).
6. Para reiniciar, pressione o botão de Reset no circuito principal.

## ✅ 8. Resultados Obtidos
A simulação demonstrou sucesso absoluto na integração dos componentes. Ao rodar o clock interno, o circuito acende corretamente os LEDs na DotMatrix emulando o display retrô. A intersecção (colisão) responde com precisão de pixels, interrompendo o clock e mantendo a integridade lógica da Máquina de Estados Finitos. O projeto atinge o nível funcional de um videogame clássico utilizando apenas eletrônica digital.

## 🔮 9. Possíveis Melhorias Futuras
- [ ] Implementar integração com componentes sonoros (buzzer/alto-falante) para som de pulo e game over.
- [ ] Adicionar suporte a displays de múltiplas cores na Matriz de LEDs.
- [ ] Criar um registrador de memória volátil para gravar a "High Score" (Pontuação Máxima) enquanto o circuito permanecer energizado.
- [ ] Implementar a mecânica de abaixar (duck) do dinossauro original.

## 👥 10. Autores
**Diogo Santos Rodrigues 082230002**

**Leonardo Rosário Teixeira 082230012**

**Bianca Ricci Lima 082230019**

**Ryan Corazza Alvarenga 082230024**

**Gustavo Sgrignoli Marmo 082230028**
