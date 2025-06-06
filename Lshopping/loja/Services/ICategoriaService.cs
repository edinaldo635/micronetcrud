using loja.Models;

namespace loja.Services;

public interface ICategoriaService
{
    Task<IEnumerable<CategoriaViewModel>> ObtemTodasCategorias();
}
