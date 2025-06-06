using System;
using System.Xml.Serialization;
using loja.Services;



var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllersWithViews();
builder.Services.AddHttpClient<IProdutoService, ProdutoService>("ProdutoApi", c =>
{
    c.BaseAddress = new Uri(builder.Configuration["ServiceUri:ProdutoApi"]); //  endereço de serviço no appsettings
});

builder.Services.AddScoped<IProdutoService, ProdutoService>();
builder.Services.AddScoped<ICategoriaService, CategoriaService>();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.Run();
