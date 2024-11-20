import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # When do we KNOW for certain that cells are mines?
        # If we have a sentence like {A, B} = 2, then both A and B MUST be mines
        # In general, if count equals number of cells, all must be mines
        if len(self.cells) == self.count and self.count != 0:
            return self.cells.copy()  # Return a copy to prevent accidental modifications
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # Similar logic: When do we KNOW cells are safe?
        # If we have a sentence like {A, B, C} = 0, then A, B, C must all be safe
        # In general, if count is 0, all cells must be safe
        if self.count == 0:
            return self.cells.copy()
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)    # Remove the cell since we now know its state
            self.count -= 1            # Reduce count since we found one of the mines

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        print(f"\nNew move: {cell} with count={count}")
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)
        print(f"Moves made: {self.moves_made}")
        # 2) mark the cell as safe
        self.mark_safe(cell)
        print(f"Known safe cells: {self.safes}")
        print(f"Known mines: {self.mines}")
        # 3) Add a new sentence to the AI's knowledge base
        neighbors = set()
        # We want to look at cells that are one away in each direction
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Skip the cell itself
                if (i, j) == cell:
                    continue
                # Make sure we're not outside the board
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbors.add((i, j))  # Add this neighbor to our set

        # Now, before we make a sentence, we need to:
        # - Remove neighbors we already know are mines (they're in self.mines)
        # - Remove neighbors we already know are safe (they're in self.safes)
        # - Adjust our count if we removed any known mines

        unknown_neighbors = set()
        mine_count = count  # This is the count parameter passed to add_knowledge

        for neighbor in neighbors:
            if neighbor in self.mines:
                # We already know it's a mine (it was marked earlier)
                # If we found a mine, we should decrease our count
                mine_count -= 1
            elif neighbor in self.safes:
                # We already know it's safe (it was marked earlier)
                # We don't need to do anything with it
                continue
            elif neighbor not in self.safes:
                # If it's not a known mine or known safe, it's unknown
                unknown_neighbors.add(neighbor)

        # Create new sentence
        if len(unknown_neighbors) > 0:
            self.knowledge.append(Sentence(unknown_neighbors, mine_count))

        # 4) mark any additional cells as safe or as mines
        # We need to look at all sentences to find new mines/safes
        while True:  # Keep checking until no new cells are marked
            new_mines = set()
            new_safes = set()

            # Look at each sentence
            for sentence in self.knowledge:
                # Get any new mines or safes from this sentence
                new_mines.update(sentence.known_mines())
                new_safes.update(sentence.known_safes())

            # If we found no new information, stop looking
            if not new_mines and not new_safes:
                break

            # Mark all new mines and safes
            for mine in new_mines:
                self.mark_mine(mine)
            for safe in new_safes:
                self.mark_safe(safe)

        # 5) add any new sentences to the AI's knowledge base
        # if they can be inferred from existing knowledge
        print("\nKnowledge base:")
        new_sentences = []
        # Compare each pair of sentences
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1.cells != sentence2.cells:  # Don't compare a sentence to itself
                    if sentence1.cells.issubset(sentence2.cells):
                        # Get the cells that are in sentence2 but not in sentence1
                        new_cells = sentence2.cells - sentence1.cells
                        # Get the new count (total mines minus mines in subset)
                        new_count = sentence2.count - sentence1.count
                        # Create and add the new sentence
                        new_sentence = Sentence(new_cells, new_count)
                        if new_sentence not in self.knowledge and new_sentence not in new_sentences:
                            new_sentences.append(new_sentence)

        # Add all new sentences to knowledge base
        self.knowledge.extend(new_sentences)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
         # Look through all cells we know are safe
        for cell in self.safes:
            # If we haven't already moved here
            if cell not in self.moves_made:
                return cell
        
        # No safe moves available
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Consider all possible cells on the board
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                # If this cell is not a move we've made and not a mine
                if cell not in self.moves_made and cell not in self.mines:
                    return cell
                    
        # No moves left to make
        return None
