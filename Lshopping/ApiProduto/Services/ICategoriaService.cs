using Lshopping.ApiProduto.DTOs;

namespace Lshopping.ApiProduto.Services;

public interface ICategoriaService
{
    Task<IEnumerable<CategoriaDTO>> ObtemCategoria();
    Task<IEnumerable<CategoriaDTO>> obtemCategoriaProduto();
    Task<CategoriaDTO> ObtemCategoriaId(int id);
    Task AdicionaCategoria(CategoriaDTO categoriaDto);
    Task AtualizaCategoria(CategoriaDTO categoriaDto);
    Task RemoveCategoria(int id);
}
