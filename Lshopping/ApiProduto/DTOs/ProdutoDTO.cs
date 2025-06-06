using System.ComponentModel;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Text.Json.Serialization;
using Lshopping.ApiProduto.Models;


namespace Lshopping.ApiProduto.DTOs;
public class ProdutoDTO
{
    public int Id { get; set; }

    [Required(ErrorMessage = "The Name is Required")]
    [MinLength(3)]
    [MaxLength(100)]
    public string Nome { get; set; }
    
    [Required(ErrorMessage = "The Description is Required")]
    [MinLength(5)]
    [MaxLength(200)]
    public string Descricao { get; set; }

    [Required(ErrorMessage = "The Price is Required")]
    [Column(TypeName = "decimal(12,2)")]
    public decimal Preco { get; set; }

    [Required(ErrorMessage = "The Stock is Required")]
    [Range(1, 9999)]
    public long Quantidade { get; set; }

    [MaxLength(250)]
    [DisplayName("Product Image")]
    public string ImagemURL { get; set; }

    public string CategoriaNome { get; set; }

    public int CategoriaId { get; set; }
    [JsonIgnore]
    public Categoria Categorias{ get; set; }   
}
    