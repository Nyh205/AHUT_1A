; Define a procedure reverse which takes in a Scheme list
; and returns a new list which is the reversed version of the original
(define (reverse lst)
    (if
        (null? lst)
        nil
        (append
            (reverse (cdr lst))
            (list (car lst))
        )
    )
)

(expect (reverse nil) ())
(expect (reverse (list 1)) (1))
(expect (reverse (list 1 2 3)) (3 2 1))
(expect (reverse (list 1 2 3 2 1)) (1 2 3 2 1))



; Define a function mountain that returns true
; if the given  list containing only positive integers and with length >= 3 is a mountain.
; A mountain is defined as a list that contains a strictly
; increasing sublist and then a strictly decreasing sublist after its "peak" number.
; (Otherwise, return false.)
(define (mountain lst)
    (define (helper lst prev state)
        (if
            (null? lst)
            ; Should only increase then decrease once
            (eq? state 'decrease)

            (begin
                (define n (car lst))
                (define rest (cdr lst))
                (cond
                    ; we just started and it's increasing, so keep going
                    ((and (> n prev) (eq? state 'start)) (helper rest n 'increase))

                    ; we just started but it's decreasing, so it's not a mountain
                    ((and (< n prev) (eq? state 'start)) #f)

                    ; it is currently increasing and we want it to increase
                    ((and (> n prev) (eq? state 'increase)) (helper rest n 'increase))

                    ; it is the start of the decrease (the peak of the mountain)
                    ((and (< n prev) (eq? state 'increase)) (helper rest n 'decrease))

                    ; it is currently increasing but we want it to decrease, so it's not a mountain
                    ((and (> n prev) (eq? state 'decrease)) #f)

                    ; it is currently decreasing and we want it to decrease
                    ((and (< n prev) (eq? state 'decrease)) (helper rest n 'decrease))

                    ; digits are equal, so it's not a mountain (we need strictly increasing/decreasing)
                    (else #f)
                )
            )

        )
    )

    (helper (cdr lst) (car lst) 'start)
)

(expect (mountain '(1 2 3 2 1)) #t)
(expect (mountain '(1 2 3 4 0)) #t)
(expect (mountain '(5 4 3 0)) #f)
(expect (mountain '(1 2 3)) #f)
(expect (mountain '(1 2 2 1)) #f)
(expect (mountain '(1 2 3 2 1 2 3)) #f)
