return {
  {
    "catppuccin/nvim",
    name = "catppuccin",
    priority = 1000,
    config = function()
      require("catppuccin").setup({
        transparent_background = true,
        integrations = {
          flash = true,
          gitsigns = true,
          lualine = true,
          nvim_surround = true,
          telescope = {
            enabled = true,
          },
          nvimtree = true,
          bufferline = true,
        },
      })

      vim.cmd.colorscheme("catppuccin")
    end,
  },
  {
    "Mofiqul/dracula.nvim",
    lazy = true,
  },
  {
    "nvim-tree/nvim-web-devicons",
    lazy = true,
  },
  {
    "nvim-lualine/lualine.nvim",
    event = "VeryLazy",
    dependencies = { "nvim-tree/nvim-web-devicons" },
    config = function()
      require("lualine").setup({
        options = {
          theme = "catppuccin-nvim",
          globalstatus = true,
          component_separators = { left = "|", right = "|" },
          section_separators = { left = "", right = "" },
        },
      })
    end,
  },
  {
    "nvim-tree/nvim-tree.lua",
    cmd = { "NvimTreeOpen", "NvimTreeToggle", "NvimTreeFocus" },
    dependencies = { "nvim-tree/nvim-web-devicons" },
    config = function()
      require("nvim-tree").setup({
        hijack_cursor = true,
        update_focused_file = {
          enable = true,
        },
        renderer = {
          group_empty = true,
        },
        view = {
          width = 34,
        },
      })
    end,
  },
  {
    "akinsho/bufferline.nvim",
    version = "*",
    event = "VeryLazy",
    dependencies = { "nvim-tree/nvim-web-devicons" },
    config = function()
      require("bufferline").setup({
        highlights = require("catppuccin.special.bufferline").get_theme(),
        options = {
          diagnostics = "nvim_lsp",
          offsets = {
            {
              filetype = "NvimTree",
              text = "File Explorer",
              highlight = "Directory",
              text_align = "left",
            },
          },
        },
      })
    end,
  },
}
