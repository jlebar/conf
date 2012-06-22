" JL 9/29/09 - Found this in my vimrc.  I'm not even sure what this is for.
set diffexpr=MyDiff()
function MyDiff()
    let opt=''
    if &diffopt =~ 'icase' | let opt = opt . '-i ' | endif
    if &diffopt =~ 'iwhite' | let opt = opt . '-b ' | endif
    silent execute '!diff -a ' . opt . v:fname_in . ' ' . v:fname_new . ' > ' . v:fname_out
endfunction

