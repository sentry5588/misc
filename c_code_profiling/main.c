void second_loop(void)
{
    
}

void first_loop(void)
{
    for (int i = 0; i < 10; i++)
    {
        second_loop();
    }
}

int main(void)
{
    for (int i = 0; i < 10; i++)
    {
        first_loop();
    }
}
