""""""""""""""""""""""""""""""""""""""""""""""""""
" Plugins Manager

call plug#begin()

" plugins
Plug 'mhinz/vim-startify'                    	" provides a start screen for Vim and Neovim
" Plug 'scrooloose/nerdtree'			" a file system explorer for the Vim editor
Plug 'vim-airline/vim-airline'			" change the default airline
" Plug 'yggdroot/indentline'			" show indent line
Plug 'tpope/vim-surround'			" provides mappings to easily delete, change and add such surroundings in pairs
Plug 'easymotion/vim-easymotion'		" a much simpler way to use some motions in vim
Plug 'tpope/vim-commentary'			" comment code
Plug 'airblade/vim-gitgutter'			" shows which lines have been added, modified, or removed

" colorscheme
Plug 'morhetz/gruvbox'
Plug 'dracula/vim', { 'as': 'dracula' }


call plug#end()

""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""
" Vim Configuration

" set colorscheme to gruvbox
" colorscheme dracula
colorscheme gruvbox

" show related row number
set nu
set rnu

" set auto indent
set autoindent

" set syntax highlight
syntax on



" show current command
set showcmd

" set backgroud color to dark
" set background=dark

" enable highlight line where cursor is
set cursorline

" set undo operation over session
set nobackup
set undofile
set undodir=~/.vim/undodir

" create undodir if not exists
if !isdirectory(&undodir)
  call mkdir(&undodir, 'p', 0700)
endif


""""""""""""""""""""""""""""""""""""""""""""""""""
" Map Setting

" set Leader Key
let mapleader=','

" use jj to jump to normal mode
" inoremap jj <Esc>

" <leader>w map to :w
inoremap <leader>w <Esc>:w<cr>
nnoremap <leader>w :w<cr>

" exit the whole vim
nnoremap <leader>q :qa<cr>

""""""""""""""""""""""""""""""""""""""""""""""""""

""""""""""""""""""""""""""""""""""""""""""""""""""
" vim-easymotion settiing

nmap <Leader>s <Plug>(easymotion-s2)

""""""""""""""""""""""""""""""""""""""""""""""""""
