; Implement a tail recursive version of reverse,
; which takes in a list and returns the reversed version of the list
; (see 19-sol.scm for non-tail recursive version)
(define (reverse lst)
    ; YOUR CODE HERE
)

; reverse tests
(expect (reverse nil) ())
(expect (reverse (list 1)) (1))
(expect (reverse (list 1 2 3)) (3 2 1))
(expect (reverse (list 1 2 3 2 1)) (1 2 3 2 1))

; map (non-tail recursive) for reference/inspiration
(define (map f lst)
    (if (null? lst)
        nil
        (cons
            (f (car lst))
            (map f (cdr lst))
        )
    )
)

; map tests
(expect (map (lambda (x) x) nil) ())
(expect (map (lambda (x) x) (list 1 2 3)) (1 2 3))
(expect (map (lambda (x) (* x x)) (list 1 2 3)) (1 4 9))
(expect (map (lambda (x) (- 5 x)) (list 1 2)) (4 3))

; Implement a tail recursive version of map
(define (map-tail f lst)
    ; YOUR CODE HERE
)

; map-tail tests (identical to map tests)
(expect (map-tail (lambda (x) x) nil) ())
(expect (map-tail (lambda (x) x) (list 1 2 3)) (1 2 3))
(expect (map-tail (lambda (x) (* x x)) (list 1 2 3)) (1 4 9))
(expect (map-tail (lambda (x) (- 5 x)) (list 1 2)) (4 3))

; Define a macro `for` that evaluates an expression for each value in a sequence
(define-macro (for sym vals expr)
    ; YOUR CODE HERE
)

; for tests
(expect (for x nil x) ())
(expect (for x '(1 2 3) x) (1 2 3))
(expect (for x '(2 3 4 5) (* x x)) (4 9 16 25))
(expect (for y '(2 4 6) (* y 3)) (6 12 18))
