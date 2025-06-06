using Lshopping.ApiProduto.Models;

namespace Lshopping.ApiProduto.Repositorio;
public interface IProdutoRepositorio
{
    Task<IEnumerable<Produto>> ObtemTodos();
    Task<Produto> ObtemId(int id);
    Task<Produto> Cadastra(Produto produto);
    Task<Produto> AtualizaProduto(Produto produto);
    Task<Produto> Exclui(int id);
}
