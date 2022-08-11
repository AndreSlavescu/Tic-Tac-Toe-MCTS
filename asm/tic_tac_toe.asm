; Author: Andre Slavescu
; Description: This program is a simple tic tac toe game.
;===============================================================

; How to play and Rules:
; 1. The game is played on a 3x3 board with the following symbols:
;    X - player 1
;    O - player 2
;    - - empty space
; 2. The game is played by entering the row and column number of the space you want to mark with your symbol.
;    For example, if you want to mark the top left space with your symbol, you would enter 1 1.
; 3. The game is over when the player enters a row and column number that is out of bounds or that is already marked.
; 4. The winner is the player who has 3 of their symbols in a row.
; 5. The game is a draw if there are no empty spaces left and no winner.
;===============================================================

; game logic

mov ax, 1
mov cl, 3
mov bl, 3

game_loop:
	
	; player 1 moves
	mov ah, 1	; input
	int 21h		; get row number
	sub al, '0'
	mov dl, al
	mov ah, 2	; output
	int 21h		; print row number

	mov ah, 1	; input
	int 21h		; get column number
	sub al, '0'
	mov dh, al
	mov ah, 2	; output
	int 21h		; print column number

	; check if row number is valid
	cmp dl, 3
	jae game_over

	; check if column number is valid
	cmp dh, 3
	jae game_over

	; check if space is empty
	mov al, [bx+dl]
	cmp al, '-'
	je game_over

	; mark space with player 1 symbol
	mov al, 'X'
	mov [bx+dl], al

	; player 2 moves
	mov ah, 1	; input
	int 21h		; get row number
	sub al, '0'
	mov dl, al
	mov ah, 2	; output
	int 21h		; print row number

	mov ah, 1	; input
	int 21h		; get column number
	sub al, '0'
	mov dh, al
	mov ah, 2	; output
	int 21h		; print column number

	; check if row number is valid
	cmp dl, 3
	jae game_over

	; check if column number is valid
	cmp dh, 3
	jae game_over

	; check if space is empty
	mov al, [bx+dl]
	cmp al, '-'
	je game_over

	; mark space with player 2 symbol
	mov al, 'O'
	mov [bx+dl], al

	; check for winner
	call check_winner

	; check for draw
	cmp cl, 0
	je game_over

	; next turn
	jmp game_loop

game_over:
	
	; print game over message
	mov ah, 9
	mov dx, offset game_over_msg
	int 21h

	; print winner message
	mov ah, 9
	cmp cl, 1
	jne print_draw
	mov dx, offset player1_win_msg
	int 21h
	jmp exit

print_draw:

	; print draw message
	mov ah, 9
	mov dx, offset draw_msg
	int 21h

exit:

	; exit program
	mov ah, 4Ch
	int 21h

check_winner:

	; check for winner in first row
	mov al, [bx]
	cmp al, 'X'
	je player1_win
	cmp al, 'O'
	je player2_win

	mov al, [bx+1]
	cmp al, 'X'
	je player1_win
	cmp al, 'O'
	je player2_win

	mov al, [bx+2]
	cmp al, 'X'
	je player1_win
	cmp al, 'O'
	je player2_win

	; check for winner in second row
	mov al, [bx+3]
	cmp al, 'X'
	je player1_win
	cmp al, 'O'
	je player2_win

	mov al, [bx+4]
	cmp al, 'X'
	je player1_win
	cmp al, 'O'
	je player2_win

	mov al, [bx+5]
	cmp al, 'X'
	je player1_win
	cmp al, 'O'
	je player2_win

	; check for winner in third row
	mov al, [bx+6]
	cmp al, 'X'
	je player1_win
	cmp al, 'O'
	je player2_win

	mov al, [bx+7]
	cmp al, 'X'
	je player1_win
	cmp al, 'O'
	je player2_win

	mov al, [bx+8]
	cmp al, 'X'
	je player1_win
	cmp al, 'O'
	je player2_win

	; check for winner in first column
	mov al, [bx]
	cmp al, 'X'
	je player1_win
	cmp al, 'O'
	je player2_win

	mov al, [bx+3]
	cmp al, 'X'
	je player1_win
	cmp al, 'O'
	je player2_win

	mov al, [bx+6]
	cmp al, 'X'
	je player1_win
	cmp al, 'O'
	je player2_win

	; check for winner in second column
	mov al, [bx+1]
	cmp al, 'X'
	je player1_win
	cmp al, 'O'
	je player2_win

	mov al, [bx+4]
	cmp al, 'X'
	je player1_win
	cmp al, 'O'
	je player2_win

	mov al, [bx+7]
	cmp al, 'X'
	je player1_win
	cmp al, 'O'
	je player2_win

	; check for winner in third column
	mov al, [bx+2]
	cmp al, 'X'
	je player1_win
	cmp al, 'O'
	je player2_win

	mov al, [bx+5]
	cmp al, 'X'
	je player1_win
	cmp al, 'O'
	je player2_win

	mov al, [bx+8]
	cmp al, 'X'
	je player1_win
	cmp al, 'O'
	je player2_win

	; check for winner in diagonal 1
	mov al, [bx]
	cmp al, 'X'
	je player1_win
	cmp al, 'O'
	je player2_win

	mov al, [bx+4]
	cmp al, 'X'
	je player1_win
	cmp al, 'O'
	je player2_win

	mov al, [bx+8]
	cmp al, 'X'
	je player1_win
	cmp al, 'O'
	je player2_win

	; check for winner in diagonal 2
	mov al, [bx+2]
	cmp al, 'X'
	je player1_win
	cmp al, 'O'
	je player2_win

	mov al, [bx+4]
	cmp al, 'X'
	je player1_win
	cmp al, 'O'
	je player2_win

	mov al, [bx+6]
	cmp al, 'X'
	je player1_win
	cmp al, 'O'
	je player2_win

player1_win:
	; player 1 wins
	mov cl, 1
	jmp game_over

player2_win:
	; player 2 wins
	mov cl, 2
	jmp game_over

; data section
game_over_msg db 'Game over.', 13, 10, '$'
player1_win_msg db 'Player 1 wins.', 13, 10, '$'
draw_msg db 'It''s a draw.', 13, 10, '$'