using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using loja.Services;
using loja.Models;

namespace loja.Services;

public class ProdutoService : IProdutoService
{
    private readonly IHttpClientFactory _clientFactory;
    private readonly JsonSerializerOptions _options;
    private const string apiEndpoint = "/api/produto/"; //endpoint para alimentação via api através do controller produto
    private ProdutoViewModel produtoVM;
    private IEnumerable<ProdutoViewModel> produtosVM;

    public ProdutoService(IHttpClientFactory clientFactory)
    {
        _clientFactory = clientFactory;
        _options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
    }

    public async Task<IEnumerable<ProdutoViewModel>> ObtemTodosProdutos()
    {
        var client = _clientFactory.CreateClient("ProdutoApi"); // ProdutoApi endereço de serviço no appsettings e que também foi configurado na classe program 

        using (var response = await client.GetAsync(apiEndpoint)) // endpoint 
        {
            if (response.IsSuccessStatusCode)
            {
                var apiResponse = await response.Content.ReadAsStreamAsync();
                produtosVM = await JsonSerializer
                            .DeserializeAsync<IEnumerable<ProdutoViewModel>>(apiResponse, _options);
            }
            else
            {
                return null;
            }
        }
        return produtosVM;
    }

   

    public async Task<ProdutoViewModel> BuscaProdutoId(int id)
    {
        var client = _clientFactory.CreateClient("ProdutoApi");
        

        using (var response = await client.GetAsync(apiEndpoint + id))
        {
            if (response.IsSuccessStatusCode)
            {
                var apiResponse = await response.Content.ReadAsStreamAsync();
                produtoVM = await JsonSerializer
                          .DeserializeAsync<ProdutoViewModel>(apiResponse, _options);
            }
            else
            {
                //throw new HttpRequestException(response.ReasonPhrase);
                return null;
            }
        }
        return produtoVM;
    }

    public async Task<ProdutoViewModel> CadastraProduto(ProdutoViewModel produtoVM)
    {
        var client = _clientFactory.CreateClient("ProdutoApi");

        StringContent content = new StringContent(JsonSerializer.Serialize(produtoVM),
                                                  Encoding.UTF8, "application/json");

        using (var response = await client.PostAsync(apiEndpoint, content))
        {
            if (response.IsSuccessStatusCode)
            {
                var apiResponse = await response.Content.ReadAsStreamAsync();
                produtoVM = await JsonSerializer
                           .DeserializeAsync<ProdutoViewModel>(apiResponse, _options);
            }
            else
            {
                return null;
                //throw new HttpRequestException(response.ReasonPhrase);
            }
        }
        return produtoVM;
    }

    public async Task<ProdutoViewModel> AtualizaProduto(ProdutoViewModel produtoVM)
    {
        var client = _clientFactory.CreateClient("ProdutoApi");

        ProdutoViewModel produtoAtualizado = new ProdutoViewModel();
        
        using (var response = await client.PutAsJsonAsync(apiEndpoint, produtoVM))
        {
            if (response.IsSuccessStatusCode)
            {
                var apiResponse = await response.Content.ReadAsStreamAsync();
                produtoAtualizado = await JsonSerializer
                                  .DeserializeAsync<ProdutoViewModel>(apiResponse, _options);
            }
            else
            {
                return null;
                //throw new HttpRequestException(response.ReasonPhrase);
            }
        }
        return produtoAtualizado;
    }

    public async Task<bool> DeletaProdutoId(int id)
    {
        var client = _clientFactory.CreateClient("ProdutoApi");

        using (var response = await client.DeleteAsync(apiEndpoint + id))
        {
            if (response.IsSuccessStatusCode)
            {
                //var apiResponse = await response.Content.ReadAsStreamAsync();
                return true;
            }
        }
        return false;
    }
}
