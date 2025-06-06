using System.ComponentModel.DataAnnotations.Schema;

namespace Lshopping.ApiProduto.Models
{
    public class Categoria
    {
        public int CategoriaId { get; set; }
        public string CategoriaNome { get; set; }
        //public ICollection<Produto> Produtos { get; set; }
        public virtual List<Produto> Produtos { get; set; }
    }
}
