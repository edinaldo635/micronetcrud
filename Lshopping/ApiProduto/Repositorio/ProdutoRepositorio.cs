using Microsoft.EntityFrameworkCore;
using ApiProduto.Context;
using Lshopping.ApiProduto.Models;

namespace Lshopping.ApiProduto.Repositorio;

public class ProdutoRepositorio : IProdutoRepositorio
{
    private readonly MyDbContext _context;
    public ProdutoRepositorio(MyDbContext context)
    {
        _context = context;
    }

    public async Task<IEnumerable<Produto>> ObtemTodos()
    {
        var produtos = await _context.Produtos.Include(c=> c.Categorias).ToListAsync();
        return produtos;
    }

    public async Task<Produto> ObtemId(int id)
    {
        return await _context.Produtos.Include(c=> c.Categorias).Where(p=> p.Id == id).FirstOrDefaultAsync();
    }

    public async Task<Produto> Cadastra(Produto produto)
    {
        _context.Produtos.Add(produto);
        await _context.SaveChangesAsync();
        return produto;
    }

    public async Task<Produto> AtualizaProduto(Produto produto)
    {
        _context.Entry(produto).State = EntityState.Modified;
        await _context.SaveChangesAsync();
        return produto;
    }

    public async Task<Produto> Exclui(int id)
    {
        var produto = await ObtemId(id);
        _context.Produtos.Remove(produto);
        await _context.SaveChangesAsync();
        return produto;
    }
}
