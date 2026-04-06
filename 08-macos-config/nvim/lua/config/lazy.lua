local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"

if not (vim.uv or vim.loop).fs_stat(lazypath) then
  local out = vim.fn.system({
    "git",
    "clone",
    "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable",
    lazypath,
  })

  if vim.v.shell_error ~= 0 then
    vim.schedule(function()
      vim.notify("Failed to bootstrap lazy.nvim:\n" .. out, vim.log.levels.ERROR)
    end)
    return
  end
end

vim.opt.rtp:prepend(lazypath)

local ok, lazy = pcall(require, "lazy")
if not ok then
  return
end

lazy.setup("plugins", {
  change_detection = {
    notify = false,
  },
})
