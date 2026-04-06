vim.g.mapleader = ","
vim.g.maplocalleader = ","

local opt = vim.opt
local undodir = vim.fn.stdpath("state") .. "/undo"

opt.number = true
opt.relativenumber = true
opt.scrolloff = 10
opt.incsearch = true
opt.autoindent = true
opt.tabstop = 4
opt.shiftwidth = 4
opt.expandtab = true
opt.showcmd = true
opt.cursorline = true
opt.backup = false
opt.writebackup = false
opt.undofile = true
opt.undodir = undodir
opt.termguicolors = true
opt.background = "dark"

if vim.fn.isdirectory(undodir) == 0 then
  vim.fn.mkdir(undodir, "p", "0700")
end

vim.cmd("syntax on")
