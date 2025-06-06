using loja.Models;

namespace loja.Services;

public interface IProdutoService
{
    Task<IEnumerable<ProdutoViewModel>> ObtemTodosProdutos();
    Task<ProdutoViewModel> BuscaProdutoId(int id);
    Task<ProdutoViewModel> CadastraProduto(ProdutoViewModel productVM);
    Task<ProdutoViewModel> AtualizaProduto(ProdutoViewModel productVM);
    Task<bool> DeletaProdutoId(int id);
}
