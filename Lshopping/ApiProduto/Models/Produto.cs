using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace Lshopping.ApiProduto.Models;

public class Produto 
{
    public int Id { get; set; }
    public string Nome { get; set; }
    public string Descricao { get;set; }
    [Column(TypeName = "decimal(12,2)")]
    public decimal Preco { get; set; }  
    public string ImagemURL { get; set; }
    public int Quantidade { get; set; }
    public int CategoriaId { get; set; }
    public virtual Categoria Categorias { get; set; }
}
