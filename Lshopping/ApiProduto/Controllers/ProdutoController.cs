using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Lshopping.ApiProduto.DTOs;
using Lshopping.ApiProduto.Services;

namespace Lshopping.ApiProduto.Controllers;

[Route("api/[controller]")]   /*aqui na api no controlador que o app. cliente acessa*/
[ApiController]
public class ProdutoController : ControllerBase
{
    private readonly IProdutoService _produtoService;
    public ProdutoController(IProdutoService produtoService)
    {
        _produtoService = produtoService;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<ProdutoDTO>>> Get()
    {
        var produtosDto = await _produtoService.ObtemProdutos();
        if (produtosDto == null)
        {
            return NotFound("Não temos este produto");
        }
        return Ok(produtosDto);
    }

    [HttpGet("{id}", Name = "ObtemProduto")]
    public async Task<ActionResult<ProdutoDTO>> Get(int id)
    {
        var produtoDto = await _produtoService.ObtemProdutoId(id);
        if (produtoDto == null)
        {
            return NotFound("Não temos este produto");
        }
        return Ok(produtoDto);
    }

    [HttpPost]
    public async Task<ActionResult> Post([FromBody] ProdutoDTO produtoDto)
    {
        if (produtoDto == null)
            return BadRequest("Dado Inválido");

        await _produtoService.AdicionaProduto(produtoDto);

        return new CreatedAtRouteResult("ObtemProduto",
            new { id = produtoDto.Id }, produtoDto);
    }

    [HttpPut]
    public async Task<ActionResult<ProdutoDTO>> Put([FromBody] ProdutoDTO produtoDto)
    {
        if (produtoDto == null)
            return BadRequest("Dado inválido");

        await _produtoService.AtualizaProduto(produtoDto);

        return Ok(produtoDto);
    }

    [HttpDelete("{id}")]
    public async Task<ActionResult<ProdutoDTO>> Delete(int id)
    {
        var produtoDto = await _produtoService.ObtemProdutoId(id);

        if (produtoDto == null)
        {
            return NotFound("Não temos este produto");
        }

        await _produtoService.RemoveProduto(id);

        return Ok(produtoDto);
    }
}