TetrisAI
========

A genetic algorithm powered Tetris AI

Execution
------------

.. code-block:: bash

    $ python god.py
    
    $ # The number of moves each Tetris AI was able to complete before losing
    $ 8 MOVES
    $ 6 MOVES
    $ 6 MOVES
    $ 6 MOVES
    $ 7 MOVES
    $ 6 MOVES
    $ 11 MOVES
    $ 11 MOVES
    $ 11 MOVES
    $ 15 MOVES
    $ 14 MOVES
    $ 20 MOVES
    $ 26 MOVES
    $ 32 MOVES
    $ 64 MOVES
    $ 143 MOVES
    $ GENERATION RESULTS:
    $ # The array represents the weights for each fitness function
    $ # The last integer is the number of moves executed before losing
    $ [6.840760499169466, -7.749389032607827, 0.6858102375895907, -1.5361113081256264]: 143
    $ [1.4849101320267017, -6.246946065548635, 3.4005829269425405, 5.42187479067551]: 64
    $ [5.917563781095321, -5.177124787019403, -8.791056447589247, -5.327712609660063]: 32
    $ [0.9257735380071157, -3.2661254932093637, -7.457388437654431, -7.330127003039877]: 26
    $ [7.084888345570697, 0.08726490011497745, 2.0595986569281486, 7.702609637569701]: 20
    $ [7.324612378993699, 5.172211228010781, 7.019656976945168, 5.482056242420768]: 15
    $ [-5.936336964875679, 0.9495197448816803, 5.033526377197697, -4.724334145761548]: 14
    $ [9.848830633446305, 4.279772154943387, 8.223934490369107, 2.8028004239357944]: 11
    $ [-7.2863188001402595, 1.0564010135470525, 3.33305956575545, 6.573176545426197]: 11
    $ [5.160973388251794, 7.844763986159521, 2.3890600482935156, 2.5184901357781015]: 11
    $ [-4.67112867937214, 5.424451694533328, 5.326128538994668, 0.09222541459832811]: 8
    $ [-5.081760655970012, 3.563066113016923, 0.941063722334242, 2.054729497306667]: 7
    $ [-2.159619111376159, 3.527618171618496, -3.845142000883934, -3.715080505095864]: 6
    $ [-3.7572634349240985, 9.050344419531157, 3.5275010647665876, -6.236516175974527]: 6
    $ [-5.647911937534111, 4.8093922973339005, -3.0575884567754574, -5.5773182414489275]: 6
    $ [4.878090208192493, 4.1322236267322445, -9.466143883438395, -8.019333614443639]: 6

and after a few generations, our AI performs better:

.. code-block:: bash

    $ GENERATION RESULTS:
    $ [0.490303559513349, -0.1780558120439566, 2.540621785232562, -2.9263626944675947]: 407
    $ [1.41096545245219, -2.890765848801392, 1.6924459243538772, -3.320989867908133]: 174
    $ [1.080068813062582, -2.5594665837528687, 2.1336079551846248, -3.39875535770893]: 167
    $ [0.818564340833499, -2.5952378193650545, 2.099336332615914, -3.0669113356082627]: 167
    $ [1.0495443362450203, -2.578687189915351, 1.8716167990668082, -3.3287900439015354]: 167
    $ [0.23403071070370768, -2.9215282195154924, 1.077423985289785, -2.531472769746995]: 135
    $ [-0.3972359239186068, -2.8907115379286394, 1.133114337100247, -3.0072110368386538]: 103
    $ [3.0522015768591437, -3.0348373671716744, 1.1336310938594125, -3.0831792420293613]: 92
    $ [1.8684085533703605, -1.9748891447683026, 0.2713095512152266, 0.5088815097570643]: 69
    $ [-0.43128491096820487, -5.247329297664674, 2.071324549770899, -3.5251769464200535]: 57
    $ [0.4187030286649307, 3.988660753279367, 0.1752543400076293, -2.8846310509430584]: 46
    $ [1.1086271019515832, -8.170689240557955, 2.077400846614997, 4.312994067460016]: 35
    $ [1.7368367017204087, -1.751632097496365, 0.8811000291929926, 2.713288446721176]: 31
    $ [0.000656935914453094, -2.6187426313439572, -8.226202273287651, -2.9223967407303286]: 29
    $ [-3.4423869646668255, -2.3023439827079155, 1.9430440220366891, -3.0518509689291653]: 24
    $ [0.19692468880062064, -2.001442828933368, 0.8750237323488945, 5.8878649517461135]: 22

Viewing The AI
------------

* To view an AI with a particular trait set, update the "trait_set.dat" file with your own weights.
* Note, you'll need to have pygame installed in your environment

.. code-block:: bash

    $ python visual_ai.py

How It Works
------------
The Tetris AI runs through every possible move for its current configuration and selects the "best" one by measuring four properties:


1. The current height of the current configuration
2. The number of sides touching in the current configuration
3. The number of "blockages" in the configuration
4. The number of rows cleared


"blockages" are defined as filled blocks that are above an empty cell in the same column. The "best" move is whichever move generates the best score, where the score is some mathematical combination of the four properties


* To evolve, we first start with a generation of 16 tetris AIs where the weights for each property is a random value from -10 to 10.
* Then we repeat the following process for several generations:
   1. We run the tetris simulations until all of them lose
   2. We select the best AI (The one that made the most number of moves before dying) and breed it with the top performing half of the population
   3. Breeding is done by averaging the trait set of the parents which generates a child trait set
   4. For each trait there is a 10% chance that instead of using the average of the parents' trait, the trait receives a random value from -10 to 10
   5. The rest of the population is filled in by breeding random pairs of AIs, making sure not to breed the same pair of AIs more than once
   6. Repeat for some number of generations until you're satisfied
