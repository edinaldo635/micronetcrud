using Lshopping.ApiProduto.Models;

namespace Lshopping.ApiProduto.Repositorio;

public interface ICategoriaRepositorio
{
    Task<IEnumerable<Categoria>> ObtemTodos();
    Task<IEnumerable<Categoria>> ObtemCategoriasdeProdutos();
    Task<Categoria> ObtemId(int id);
    Task<Categoria> Cadastra(Categoria categoria);
    Task<Categoria> Atualiza(Categoria categoria);
    Task<Categoria> Exclui(int id);
}
