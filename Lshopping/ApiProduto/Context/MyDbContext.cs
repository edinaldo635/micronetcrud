//aqui é mapeado as entidade e as tabelas e definido propriedades para gerar os nomes de campos das tabelas
using Microsoft.EntityFrameworkCore;
using Lshopping.ApiProduto.Models;


namespace ApiProduto.Context
{
    
    public class MyDbContext : DbContext
    {
        public MyDbContext(DbContextOptions<MyDbContext> options) : base(options) { }

        public DbSet<Categoria> Categorias { get; set; }
        public DbSet<Produto> Produtos { get; set; }
        // ia trabalhar com base oracle
        /*protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder.UseOracle(@"User Id=blog;Password=<password>;Data Source=pdborcl;");
        }*/

        //Aqui é usado Fluent API para realizar espeficicações das propriedades
        protected override void OnModelCreating(ModelBuilder mb)
        {
            //category

            mb.Entity<Categoria>().HasKey(c => c.CategoriaId);

            mb.Entity<Categoria>().
                 Property(c => c.CategoriaNome).
                   HasMaxLength(100).
                        IsRequired();
            //Product
            mb.Entity<Produto>().
               Property(c => c.Nome).
                 HasMaxLength(100).
                   IsRequired();

            mb.Entity<Produto>().
              Property(c => c.Descricao).
                   HasMaxLength(255).
                       IsRequired();

            mb.Entity<Produto>().
              Property(c => c.ImagemURL).
                  HasMaxLength(255).
                      IsRequired();

            mb.Entity<Produto>().
               Property(c => c.Preco).
                 HasPrecision(12, 2);

            mb.Entity<Categoria>()
              .HasMany(g => g.Produtos)
                .WithOne(c => c.Categorias)
                .IsRequired()
                  .OnDelete(DeleteBehavior.Cascade);

            mb.Entity<Categoria>().HasData(
                new Categoria
                {
                    CategoriaId = 1,
                    CategoriaNome = "Material Escolar",
                },
                new Categoria
                {
                    CategoriaId = 2,
                    CategoriaNome = "Acessórios",
                },
                new Categoria
                {
                    CategoriaId = 3,
                    CategoriaNome = "Eletrodomésticos",
                },
                new Categoria
                {
                    CategoriaId = 4,
                    CategoriaNome = "Celulares",
                },
                new Categoria
                {
                    CategoriaId = 5,
                    CategoriaNome = "Informática",
                },
                new Categoria
                {
                    CategoriaId = 6,
                    CategoriaNome = "Eletrônicos",
                },
                new Categoria
                {
                    CategoriaId = 7,
                    CategoriaNome = "Produtos do lar",
                },
                new Categoria
                {
                    CategoriaId = 8,
                    CategoriaNome = "Vestuário",
                },
                new Categoria
                {
                    CategoriaId = 9,
                    CategoriaNome = "Calçados",
                },
                new Categoria
                {
                    CategoriaId = 10,
                    CategoriaNome = "Móveis",
                }
            );
        }
    }
}
