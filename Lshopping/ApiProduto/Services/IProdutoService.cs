using Lshopping.ApiProduto.DTOs;

namespace Lshopping.ApiProduto.Services;

public interface IProdutoService
{
    Task<IEnumerable<ProdutoDTO>> ObtemProdutos();
    Task<ProdutoDTO> ObtemProdutoId(int id);
    Task AdicionaProduto(ProdutoDTO produtoDto);
    Task AtualizaProduto(ProdutoDTO produtoDto);
    Task RemoveProduto(int id);
}
