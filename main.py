import pygame

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 512, 512
SQ_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Unicode Chess")
font = pygame.font.SysFont("Segoe UI Symbol", 50) # Supports Unicode Chess Pieces

# Piece Representations
PIECES = {
    'bR': '♜', 'bN': '♞', 'bB': '♝', 'bQ': '♛', 'bK': '♚', 'bp': '♟',
    'wR': '♖', 'wN': '♘', 'wB': '♗', 'wQ': '♕', 'wK': '♔', 'wp': '♙'
}

class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp"] * 8, ["--"] * 8, ["--"] * 8, ["--"] * 8, ["--"] * 8,
            ["wp"] * 8, ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.white_to_move = True
        self.selected_sq = None

    def handle_click(self, pos):
        col, row = pos[0] // SQ_SIZE, pos[1] // SQ_SIZE
        
        if self.selected_sq:
            # Move Piece
            r1, c1 = self.selected_sq
            piece = self.board[r1][c1]
            
            # Simple Validation: Don't capture your own color
            target = self.board[row][col]
            if target == "--" or target[0] != piece[0]:
                self.board[row][col] = piece
                self.board[r1][c1] = "--"
                self.white_to_move = not self.white_to_move
            
            self.selected_sq = None
        else:
            # Select Piece (only if it's your turn)
            piece = self.board[row][col]
            if piece != "--":
                if (self.white_to_move and piece[0] == 'w') or (not self.white_to_move and piece[0] == 'b'):
                    self.selected_sq = (row, col)

def draw_game(gs):
    colors = [pygame.Color(235, 235, 208), pygame.Color(119, 148, 85)]
    for r in range(8):
        for c in range(8):
            # Draw Square
            color = colors[(r + c) % 2]
            if gs.selected_sq == (r, c): color = pygame.Color("yellow") # Highlight selected
            pygame.draw.rect(screen, color, (c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            
            # Draw Piece
            piece = gs.board[r][c]
            if piece != "--":
                text_surface = font.render(PIECES[piece], True, (0, 0, 0))
                # Center the piece in the square
                text_rect = text_surface.get_rect(center=(c*SQ_SIZE + SQ_SIZE//2, r*SQ_SIZE + SQ_SIZE//2))
                screen.blit(text_surface, text_rect)

def main():
    gs = GameState()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                gs.handle_click(pygame.mouse.get_pos())

        draw_game(gs)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()