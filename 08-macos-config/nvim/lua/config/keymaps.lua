local map = vim.keymap.set

map("n", "Q", "gq", { silent = true, desc = "Format text with gq" })

map("n", "<leader>w", "<cmd>w<cr>", { silent = true, desc = "Save current buffer" })
map("i", "<leader>w", "<Esc><cmd>w<cr>", { silent = true, desc = "Save current buffer" })
map("n", "<leader>q", "<cmd>qa<cr>", { silent = true, desc = "Quit Neovim" })

map("n", "<leader>g", "<cmd>Telescope find_files<cr>", { silent = true, desc = "Find files" })
map("n", "<leader>f", "<cmd>Telescope live_grep<cr>", { silent = true, desc = "Find in project" })
map("n", "<leader>1", "<cmd>NvimTreeToggle<cr>", { silent = true, desc = "Toggle nvim-tree" })
map("n", "<leader>c", "<cmd>bdelete<cr>", { silent = true, desc = "Close current buffer" })
map("n", "<S-l>", "<cmd>BufferLineCycleNext<cr>", { silent = true, desc = "Next buffer" })
map("n", "<S-h>", "<cmd>BufferLineCyclePrev<cr>", { silent = true, desc = "Previous buffer" })
map("n", "<leader>s", function()
  require("flash").jump()
end, { silent = true, desc = "Flash jump" })

map("n", "<leader>r", function()
  if #vim.lsp.get_clients({ bufnr = 0 }) > 0 then
    vim.lsp.buf.format({ async = true })
    return
  end

  local view = vim.fn.winsaveview()
  vim.cmd("normal! gg=G")
  vim.fn.winrestview(view)
end, { desc = "Format buffer" })
