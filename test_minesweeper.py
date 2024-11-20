# test_minesweeper.py
from minesweeper import MinesweeperAI, Sentence

def test_ai():
    # Create an AI instance
    ai = MinesweeperAI()
    
    # Test a simple scenario
    print("Test 1: Single cell with no mines nearby")
    ai.add_knowledge((0,0), 0)  # Corner cell with no mines
    print("Expected: All neighbors should be marked safe")
    
    print("\nTest 2: Cell with one mine nearby")
    ai.add_knowledge((2,2), 1)  # Middle cell with one mine
    print("Current knowledge base:")
    for sentence in ai.knowledge:
        print(sentence)
        
    # Make a move
    move = ai.make_safe_move()
    print(f"AI's safe move: {move}")

def test_subset_inference():
    ai = MinesweeperAI()
    
    print("Starting inference test...")
    print("\nStep 1: Adding two related sentences")
    # First sentence: one of {A,B} is a mine
    sentence1 = Sentence({(0,0), (0,1)}, 1)
    # Second sentence: two of {A,B,C} are mines
    sentence2 = Sentence({(0,0), (0,1), (0,2)}, 2)
    
    ai.knowledge.append(sentence1)
    ai.knowledge.append(sentence2)
    
    print("Initial knowledge base:")
    for sentence in ai.knowledge:
        print(f"Sentence: {sentence}")
        
    print("\nStep 2: Inferring new sentence...")
    # If one of {A,B} is a mine (sentence1)
    # And two of {A,B,C} are mines (sentence2)
    # Then: C must be a mine! (because sentence2 - sentence1 = {C} = 1)
    
    # Let's modify our add_knowledge code to test this:
    new_sentences = []
    for s1 in ai.knowledge:
        for s2 in ai.knowledge:
            if s1.cells and s2.cells and s1.cells != s2.cells:  # Check cells aren't empty
                if s1.cells.issubset(s2.cells):
                    new_cells = s2.cells - s1.cells
                    new_count = s2.count - s1.count
                    new_sentence = Sentence(new_cells, new_count)
                    print(f"\nFound inference:")
                    print(f"From {s1} and {s2}")
                    print(f"We can infer: {new_sentence}")
                    if new_cells:  # Only add if we have cells
                        new_sentences.append(new_sentence)
    
    ai.knowledge.extend(new_sentences)
    
    print("\nFinal knowledge base:")
    for sentence in ai.knowledge:
        print(f"Sentence: {sentence}")

def test_realistic_inference():
    ai = MinesweeperAI()
    
    print("Realistic game scenario...")
    
    # Step 1: We click (0,0) and find out it has 2 mines around it
    print("\nStep 1: We clicked (0,0) and found 2 mines nearby")
    ai.add_knowledge((0,0), 2)
    
    print("\nAfter clicking (0,0):")
    print(f"Known safe cells: {ai.safes}")  # Should include (0,0)
    print(f"Moves made: {ai.moves_made}")   # Should include (0,0)
    print("Knowledge base:")
    for sentence in ai.knowledge:
        print(f"Sentence: {sentence}")
    
    # Step 2: We click (1,1) and find out it has 0 mines around it
    print("\nStep 2: We clicked (1,1) and found 0 mines nearby")
    ai.add_knowledge((1,1), 0)
    
    print("\nAfter clicking (1,1):")
    print(f"Known safe cells: {ai.safes}")  
    print(f"Known mines: {ai.mines}")
    print("Knowledge base:")
    for sentence in ai.knowledge:
        print(f"Sentence: {sentence}")

def test_safe_move():
    ai = MinesweeperAI(height=3, width=3)  # Small 3x3 board
    
    print("Testing safe moves...")
    
    # Initially no safe moves known
    print("\nStep 1: Initial state")
    move = ai.make_safe_move()
    print(f"Safe move available: {move}")  # Should be None
    
    # Mark some cells as safe
    print("\nStep 2: Mark (0,0) and (1,1) as safe")
    ai.mark_safe((0,0))
    ai.mark_safe((1,1))
    move = ai.make_safe_move()
    print(f"Safe move available: {move}")  # Should return either (0,0) or (1,1)
    
    # Make a move
    print("\nStep 3: Make move to", move)
    ai.moves_made.add(move)
    move = ai.make_safe_move()
    print(f"Next safe move available: {move}")  # Should return the other safe cell
    
    # Make another move
    print("\nStep 4: Make move to", move)
    ai.moves_made.add(move)
    move = ai.make_safe_move()
    print(f"Any safe moves left? {move}")  # Should be None
  
def test_random_move():
    ai = MinesweeperAI(height=3, width=3)  # Small 3x3 board for testing
    
    print("Testing random moves...")
    
    # Step 1: Initial state (all moves should be available except mines/moves made)
    print("\nStep 1: Initial state (empty 3x3 board)")
    move = ai.make_random_move()
    print(f"First random move: {move}")  # Should return any cell
    
    # Step 2: Mark some cells as mines and make some moves
    print("\nStep 2: Mark some cells as mines and make some moves")
    ai.mark_mine((0, 0))  # Mark top-left as mine
    ai.mark_mine((0, 1))  # Mark top-middle as mine
    ai.moves_made.add((1, 1))  # Mark center as moved
    print(f"Mines: {ai.mines}")
    print(f"Moves made: {ai.moves_made}")
    
    # Try getting several random moves
    print("\nStep 3: Get multiple random moves")
    available_moves = set()
    for _ in range(5):  # Try 5 times
        move = ai.make_random_move()
        if move:
            available_moves.add(move)
    print(f"Available moves found: {available_moves}")
    
    # Step 4: Fill almost all cells and verify remaining move
    print("\nStep 4: Fill most cells, leaving only one valid move")
    ai.moves_made.add((0, 2))
    ai.moves_made.add((1, 0))
    ai.moves_made.add((1, 2))
    ai.moves_made.add((2, 0))
    ai.moves_made.add((2, 1))
    print(f"Moves made: {ai.moves_made}")
    print(f"Mines: {ai.mines}")
    move = ai.make_random_move()
    print(f"Only remaining move: {move}")  # Should be (2,2)
    
    # Step 5: Fill all cells and verify no moves remain
    print("\nStep 5: Fill all cells and verify no moves remain")
    ai.moves_made.add((2, 2))
    move = ai.make_random_move()
    print(f"Any moves left? {move}")  # Should be None

if __name__ == "__main__":
    # test_ai()
    # test_subset_inference()
    # test_realistic_inference()
    # test_safe_move()
    test_random_move()