using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Lshopping.ApiProduto.DTOs;
using Lshopping.ApiProduto.Services;

namespace Lshopping.ApiProduto.Controllers;

[Route("api/[controller]")]
[ApiController]
public class CategoriaController : ControllerBase
{
    private readonly ICategoriaService _categoriaService;
    public CategoriaController(ICategoriaService categoriaService)
    {
        _categoriaService = categoriaService;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<CategoriaDTO>>> Get()
    {
        var categoriasDto = await _categoriaService.ObtemCategoria();
        if (categoriasDto == null)
        {
            return NotFound("Está categoria ainda não existe");
        }
        return Ok(categoriasDto);
    }

    [HttpGet("produtos")]
    public async Task<ActionResult<IEnumerable<CategoriaDTO>>> GetCategoriasProducts()
    {
        var categoriasDto = await _categoriaService.obtemCategoriaProduto();
        if (categoriasDto == null)
        {
            return NotFound("Está categoria ainda não existe");
        }
        return Ok(categoriasDto);
    }

    [HttpGet("{id:int}", Name = "ObtemCategoria")]
    public async Task<ActionResult<CategoriaDTO>> Get(int id)
    {
        var categoriaDto = await _categoriaService.ObtemCategoriaId(id);
        if (categoriaDto == null)
        {
            return NotFound("Está categoria ainda não existe");
        }
        return Ok(categoriaDto);
    }

    [HttpPost]
    public async Task<ActionResult> Post([FromBody] CategoriaDTO categoriaDto)
    {
        if (categoriaDto == null)
            return BadRequest("Invalid Data");

        await _categoriaService.AdicionaCategoria(categoriaDto);

        return new CreatedAtRouteResult("ObtemCategoria\"", new { id = categoriaDto.CategoriaId },
            categoriaDto);
    }

    [HttpPut("{id:int}")]
    public async Task<ActionResult> Put(int id, [FromBody] CategoriaDTO categoriaDto)
    {
        if (id != categoriaDto.CategoriaId)
            return BadRequest();

        if (categoriaDto == null)
            return BadRequest();

        await _categoriaService.AtualizaCategoria(categoriaDto);

        return Ok(categoriaDto);
    }

    [HttpDelete("{id:int}")]
    public async Task<ActionResult<CategoriaDTO>> Delete(int id)
    {
        var categoriaDto = await _categoriaService.ObtemCategoriaId(id);
        if (categoriaDto == null)
        {
            return NotFound("Category not found");
        }

        await _categoriaService.RemoveCategoria(id);

        return Ok(categoriaDto);
    }
}
