using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace loja.Models;

public class ProdutoViewModel
{
    public int Id { get; set; }
    [Required]
    public string Nome { get; set; }
    [Required]
    public string Descricao { get; set; }

    [Required]
    [Range(1,9999)]
    [Column(TypeName = "decimal(12,2)")]
    public decimal Preco { get; set; }
    [Required]
    [Display(Name = "Imagem URL")]
    public string ImagemURL { get; set; }

    [Range(1, 100)]
    public int Quantidade { get; set; } = 1;

    [Display(Name="Categoria")]
    public int CategoriaId { get; set; }
}
