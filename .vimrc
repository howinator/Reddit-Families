filetype on
filetype plugin on
filetype plugin indent on
:au BufNewFile,BufRead *.f90 set filetype=fortran
:let fortran_free_source=1
:set expandtab
:set shiftwidth=2
:set tabstop=2
:set tw=128
:set autoindent
set title
autocmd FileType make set noexpandtab shiftwidth=8 softtabstop=0
syntax enable
set number
syntax on
filetype indent on
:set ru
