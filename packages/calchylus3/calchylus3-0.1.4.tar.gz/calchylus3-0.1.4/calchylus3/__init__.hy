#! /usr/bin/env hy
;----------------------------------------------
; Calchylus 3 - Lambda calculus with Hy
;
; Source:
; https://github.com/markomanninen/calchylus3/
;
; Install:
; $ pip install calchylus3
;
; Open Hy:
; $ hy
;
; Import library:
; (require [calchylus3.lambdas [*]])
;
; Initialize with macros:
; (with-macros λ)
;
; or without macros
; (without-macros λ)
;
; For example church number two:
; ((λ x y [x [x y]]) 'a 'b) -> (a (a b))
;
; or if macros are included, then:
; (TWO 'a 'b) -> (a (a b))
;
; Documentation: http://calchylus3.readthedocs.io/
; Author: Marko Manninen <elonmedia@gmail.com>
; Copyright: Marko Manninen (c) 2019
; Licence: MIT
;----------------------------------------------

(setv __version__ "0.1.4")
