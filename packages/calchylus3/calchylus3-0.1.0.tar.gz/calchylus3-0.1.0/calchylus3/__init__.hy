#! /usr/bin/env hy
;----------------------------------------------
; Calchylus - Lambda calculus with Hy
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
; (import [calchylus3.lambdas [*]])
;
; Initialize macros:
; (with-macros L)
;
; Use:
; (L x y (x (x y)) a b) ->
; (a (a b))
;
; Documentation: http://calchylus3.readthedocs.io/
; Author: Marko Manninen <elonmedia@gmail.com>
; Copyright: Marko Manninen (c) 2019
; Licence: MIT
;----------------------------------------------

(setv __version__ "v0.1.0")
