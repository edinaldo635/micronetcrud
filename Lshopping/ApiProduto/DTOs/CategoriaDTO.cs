using System.ComponentModel.DataAnnotations;
using Lshopping.ApiProduto.Models;

namespace Lshopping.ApiProduto.DTOs;

public class CategoriaDTO
{
    public int CategoriaId { get; set; }

    [Required(ErrorMessage = "The Name is Required")]
    [MinLength(3)]
    [MaxLength(100)]
    public string Nome { get; set; }

    public ICollection<Produto> Produtos { get; set; }
}
