using System.ComponentModel.DataAnnotations;

namespace loja.Models;
public class CategoriaViewModel
{
    public int CategoriaId { get; set; }
    [Required]
    public string CategoriaNome { get; set; }
}
