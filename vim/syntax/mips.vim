" Vim syntax file
" Language   : MIPS assembly
" Maintainers: Justin Lebar
" Revision   : Nov 14, 2009

if version < 600
  syntax clear
elseif exists("b:current_syntax")
  finish
endif

syn case match
syn sync minlines=50

syn match mipsDirective "^\s*\.\(align\|ascii\|byte\|data\|globl\|text\|word\)"
syn match mipsLabel "^.*:$"

syn match mipsComment "#.*" 

hi link mipsDirective PreProc
hi link mipsComment Comment
hi link mipsLabel Label
