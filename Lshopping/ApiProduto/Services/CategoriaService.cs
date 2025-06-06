using AutoMapper;
using Lshopping.ApiProduto.Repositorio;
using Lshopping.ApiProduto.DTOs;
using Lshopping.ApiProduto.Models;

namespace Lshopping.ApiProduto.Services;

public class CategoriaService : ICategoriaService
{
    private ICategoriaRepositorio _categoriaRepositorio;
    private readonly IMapper _mapper; // variavel interface do automapper para fazer a injeção de dependência no construtor do serviço abaixo
    public CategoriaService(ICategoriaRepositorio categoriaRepositorio, IMapper mapper)
    {
        _categoriaRepositorio = categoriaRepositorio;
        _mapper = mapper;
    }

    public async Task<IEnumerable<CategoriaDTO>> ObtemCategoria()
    {
        var categoriaEntity = await _categoriaRepositorio.ObtemTodos();
        return _mapper.Map<IEnumerable<CategoriaDTO>>(categoriaEntity);
    }

    public async Task<IEnumerable<CategoriaDTO>> obtemCategoriaProduto()
    {
        var categoriaEntity = await _categoriaRepositorio.ObtemCategoriasdeProdutos();
        return _mapper.Map<IEnumerable<CategoriaDTO>>(categoriaEntity);
    }


    public async Task<CategoriaDTO> ObtemCategoriaId(int id)
    {
        var categoriaEntity = await _categoriaRepositorio.ObtemId(id);
        return _mapper.Map<CategoriaDTO>(categoriaEntity);
    }

    public async Task AdicionaCategoria(CategoriaDTO categoriaDto)
    {
        var categoriaEntity = _mapper.Map<Categoria>(categoriaDto);
        await _categoriaRepositorio.Cadastra(categoriaEntity);
        categoriaDto.CategoriaId = categoriaEntity.CategoriaId;
    }

    public async Task AtualizaCategoria(CategoriaDTO categoriaDto)
    {
        var categoriaEntity = _mapper.Map<Categoria>(categoriaDto);
        await _categoriaRepositorio.Atualiza(categoriaEntity);
    }

    public async Task RemoveCategoria(int id)
    {
        var categoriaEntity = _categoriaRepositorio.ObtemId(id).Result;
        await _categoriaRepositorio.Exclui(categoriaEntity.CategoriaId);
    }
}
