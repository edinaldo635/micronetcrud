using System.Net.Http.Headers;
using System.Text.Json;
using loja.Models;
namespace loja.Services;

public class CategoriaService : ICategoriaService
{
    private readonly IHttpClientFactory _clientFactory;
    private readonly JsonSerializerOptions _options;
    private const string apiEndpoint = "/api/categorias/";

    public CategoriaService(IHttpClientFactory clientFactory)
    {
        _clientFactory = clientFactory;
        _options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
    }

    public async Task<IEnumerable<CategoriaViewModel>> ObtemTodasCategorias()
    {
        var client = _clientFactory.CreateClient("ProdutoApi");
        
        IEnumerable<CategoriaViewModel> categorias;

        using (var response = await client.GetAsync(apiEndpoint))
        {

            if (response.IsSuccessStatusCode)
            {
                var apiResponse = await response.Content.ReadAsStreamAsync();
                categorias = await JsonSerializer
                          .DeserializeAsync<IEnumerable<CategoriaViewModel>>(apiResponse, _options);
            }
            else
            {
                throw new HttpRequestException(response.ReasonPhrase);
            }
        }
        return categorias;
    }
}
