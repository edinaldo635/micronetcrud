using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using loja.Models;
using loja.Services;
namespace loja.Controllers;
public class ProdutoController : Controller
{
    private readonly IProdutoService _produtoService;
    private readonly ICategoriaService _categoriaService;
    private readonly IWebHostEnvironment _webHostEnvironment;
    public ProdutoController(IProdutoService produtoService,
                            ICategoriaService categoriaService,
                            IWebHostEnvironment webHostEnvironment)
    {
        _produtoService = produtoService;
        _categoriaService = categoriaService;
        _webHostEnvironment = webHostEnvironment;
    }

    [HttpGet]
    public async Task<ActionResult<IEnumerable<ProdutoViewModel>>> Index()
    {
        
        var result = await _produtoService.ObtemTodosProdutos();

        if (result is null)
            return View("Error");

        return View(result);
    }

    public  IActionResult CadastraProduto()
    {
        return View();
    }

    [HttpPost]
    public async Task<IActionResult> CadastraProduto(ProdutoViewModel produtoVM)
    {
        if (ModelState.IsValid)
        {
            var result = await _produtoService.CadastraProduto(produtoVM);

            if (result != null)
                return RedirectToAction(nameof(Index));
        }
        
        return View(produtoVM);
    }
    [HttpGet]
    public async Task<IActionResult> AtualizaProduto(int id)
    {
        
        var result = await _produtoService.BuscaProdutoId(id);

        if (result is null)
            return View("Error");

        return View(result);
    }

    [HttpPost]
    public async Task<IActionResult> AtualizaProduto(ProdutoViewModel produtoVM)
    {
        if (ModelState.IsValid)
        {
            var result = await _produtoService.AtualizaProduto(produtoVM);

            if (result is not null)
                return RedirectToAction(nameof(Index));
        }
        return View(produtoVM);
    }

    [HttpGet]
    public async Task<ActionResult<ProdutoViewModel>> DeletaProduto(int id)
    {
        var result = await _produtoService.BuscaProdutoId(id);

        if (result is null)
            return View("Error");

        return View(result);
    }

    [HttpPost(), ActionName("DeletaProduto")]
    public async Task<IActionResult> DeleteConfirmed(int id)
    {
        var result = await _produtoService.DeletaProdutoId(id);

        if (!result)
            return View("Error");

        return RedirectToAction("Index");
    }
}
