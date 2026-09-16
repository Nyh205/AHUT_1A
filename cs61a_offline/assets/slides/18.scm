; Define a procedure summation which takes in 2 arguments
; n (a non-negative integer) and term (a procedure)
; and returns the summation of calling term on each
; integer from 0 to n, inclusive.
(define (summation n term)
    ; YOUR CODE HERE
)

; Unit tests
(define (identity x) x)
(define (square x) (* x x))
(define (add-one x) (+ x 1))
(expect (summation 0 identity) 0)

; 0 + 1 + 2 + 3 + 4 + 5 = 15
(expect (summation 5 identity) 15)

; 0^2 + 1^2 + 2^2 + 3^2 + 4^2 + 5^2
; = 1 + 4 + 9 + 16 + 25
; = 55
(expect (summation 5 square) 55)

; (0+1) + (1+1) + (2+1) + (3+1)
; = 1 + 2 + 3 + 4
; = 10
(expect (summation 3 add-one) 10)



; Define a function sum-even which sums the digits
; at even positions in a positive integer n,
; where position 0 is the rightmost digit, position 1 is
; the digit to its left, etc.
(define (sum-even n)
    ; YOUR CODE HERE
)

(expect (sum-even 5) 5)
(expect (sum-even 10) 0)
(expect (sum-even 12321) 5) ; 1 + 3 + 1 = 5
(expect (sum-even 1112) 3) ; 2 + 1 = 3
