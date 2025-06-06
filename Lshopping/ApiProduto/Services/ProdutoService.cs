using AutoMapper;
using Lshopping.ApiProduto.DTOs;
using Lshopping.ApiProduto.Models;
using Lshopping.ApiProduto.Repositorio;

namespace Lshopping.ApiProduto.Services;

public class ProdutoService : IProdutoService
{
    private readonly IMapper _mapper;
    private IProdutoRepositorio _produtoRepositorio;

    public ProdutoService(IMapper mapper, IProdutoRepositorio produtoRepositorio)
    {
        _mapper = mapper;
        _produtoRepositorio = produtoRepositorio;
    }

    public async Task<IEnumerable<ProdutoDTO>> ObtemProdutos()
    {
        var produtosEntity = await _produtoRepositorio.ObtemTodos();
        return _mapper.Map<IEnumerable<ProdutoDTO>>(produtosEntity);
    }

    public async Task<ProdutoDTO> ObtemProdutoId(int id)
    {
        var produtoEntity = await _produtoRepositorio.ObtemId(id);
        return _mapper.Map<ProdutoDTO>(produtoEntity);
    }
    public async Task AdicionaProduto(ProdutoDTO produtoDto)
    {
        var produtoEntity = _mapper.Map<Produto>(produtoDto);
        await _produtoRepositorio.Cadastra(produtoEntity);
        produtoDto.Id = produtoEntity.Id;
    }

    public async Task AtualizaProduto(ProdutoDTO productDto)
    {
        var categoriaEntity = _mapper.Map<Produto>(productDto);
        await _produtoRepositorio.AtualizaProduto(categoriaEntity);
    }


    public async Task RemoveProduto(int id)
    {
        var produtoEntity = await _produtoRepositorio.ObtemId(id);
        await _produtoRepositorio.Exclui(produtoEntity.Id);
    }
}
