using AutoMapper;
using Lshopping.ApiProduto.Models;

namespace Lshopping.ApiProduto.DTOs.Mappings;

public class MappingProfile : Profile
{
    public MappingProfile()
    {
        CreateMap<Categoria, CategoriaDTO>().ReverseMap();
        
        CreateMap<ProdutoDTO, Produto>();
        CreateMap<Produto, ProdutoDTO>()
         .ForMember(x => x.CategoriaNome, opt => opt.MapFrom(src => src.Categorias.CategoriaNome));/*quando eu mapear de product pra product dto eu uso um recurso do automaper onde eu defino que a propriedade category nome será mapeada com o valor que eu obtenho via map from do automaper da propriedade de navegação category como fonte entao obtem o valor de category nome a partir de category do nome da categoria*/
        
    }
}
