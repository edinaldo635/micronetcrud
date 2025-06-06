using Microsoft.EntityFrameworkCore;
using Lshopping.ApiProduto.Models;
using ApiProduto.Context;

namespace Lshopping.ApiProduto.Repositorio;

public class CategoriaRepositorio : ICategoriaRepositorio
{
    private readonly MyDbContext _context;
    public CategoriaRepositorio(MyDbContext context)
    {
        _context = context;
    }

    public async Task<IEnumerable<Categoria>> ObtemTodos()
    {
        return await _context.Categorias.ToListAsync();
    }

    public async Task<IEnumerable<Categoria>> ObtemCategoriasdeProdutos()
    {
        return await _context.Categorias.Include(x => x.Produtos).ToListAsync();
    }

    public async Task<Categoria> ObtemId(int id)
    {
        return await _context.Categorias.Where(p => p.CategoriaId == id).FirstOrDefaultAsync();
    }

    public async Task<Categoria> Cadastra(Categoria categoria)
    {
        _context.Categorias.Add(categoria);
        await _context.SaveChangesAsync();
        return categoria;
    }

    public async Task<Categoria> Atualiza(Categoria categoria)
    {
        _context.Entry(categoria).State = EntityState.Modified;
        await _context.SaveChangesAsync();
        return categoria;
    }

    public async Task<Categoria> Exclui(int id)
    {
        var produto = await ObtemId(id);
        _context.Categorias.Remove(produto);
        await _context.SaveChangesAsync();
        return produto;
    }
}
