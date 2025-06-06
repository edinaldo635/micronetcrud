using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using loja.Models;
using loja.Services;

namespace loja.Controllers;

public class HomeController : Controller
{
    private readonly ILogger<HomeController> _logger;
    private readonly IProdutoService _produtoService;
    private readonly ICategoriaService _categoriaService;
    public HomeController(ILogger<HomeController> logger,
        IProdutoService produtoService, ICategoriaService categoriaService)
    {
        _logger = logger;
        _produtoService = produtoService;
        _categoriaService = categoriaService;
    }

    public async Task<IActionResult> Index()
    {
        var produtos = await _produtoService.ObtemTodosProdutos();

        if (produtos is null)
        {
            return View("Error");
        }

        return View(produtos);
    }

    [HttpGet]
    public async Task<ActionResult<ProdutoViewModel>> ProdutoDetails(int id)
    {
        var produto = await _produtoService.BuscaProdutoId(id);

        if (produto is null)
            return View("Error");

        return View(produto);
    }
    public IActionResult CadastraCategoria()
    {
        return View();
    }

    [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
    public IActionResult Error(string message)
    {
        return View(new ErrorViewModel { ErrorMessage = message });
    }


}